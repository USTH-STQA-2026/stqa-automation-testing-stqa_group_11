"""
web_detector.py — Tự động nhận diện công nghệ web và chọn chiến lược tương tác.

Hỗ trợ phát hiện:
  - Flutter Web (CanvasKit / HTML renderer)
  - React / Next.js
  - Angular
  - Vue.js / Nuxt.js
  - HTML thuần (static)

Sử dụng:
    from web_detector import detect_technology, WebTech
    tech = detect_technology(page)
    print(tech.name, tech.renderer)
"""
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TechName(str, Enum):
    FLUTTER = "Flutter Web"
    REACT = "React"
    NEXTJS = "Next.js"
    ANGULAR = "Angular"
    VUE = "Vue.js"
    NUXTJS = "Nuxt.js"
    SVELTE = "Svelte"
    STATIC_HTML = "HTML thuần / Static"
    UNKNOWN = "Không xác định"


class FlutterRenderer(str, Enum):
    CANVASKIT = "CanvasKit"
    HTML = "HTML"
    UNKNOWN = "Không xác định"


@dataclass
class WebTech:
    name: TechName
    renderer: Optional[str] = None  # Dành cho Flutter (CanvasKit / HTML)
    version: Optional[str] = None
    evidence: list = field(default_factory=list)  # Danh sách bằng chứng phát hiện

    @property
    def is_flutter(self) -> bool:
        return self.name == TechName.FLUTTER

    @property
    def is_flutter_canvaskit(self) -> bool:
        return self.name == TechName.FLUTTER and self.renderer == FlutterRenderer.CANVASKIT

    @property
    def needs_semantics(self) -> bool:
        """Flutter CanvasKit cần bật semantics tree để tương tác."""
        return self.is_flutter_canvaskit

    @property
    def uses_standard_dom(self) -> bool:
        """Có dùng DOM HTML tiêu chuẩn (input, button, ...) hay không."""
        return not self.is_flutter_canvaskit

    def summary(self) -> str:
        lines = [f"Công nghệ: {self.name.value}"]
        if self.renderer:
            lines.append(f"Renderer: {self.renderer}")
        if self.version:
            lines.append(f"Version: {self.version}")
        lines.append(f"DOM tiêu chuẩn: {'Có' if self.uses_standard_dom else 'Không'}")
        lines.append(f"Cần bật Semantics: {'Có' if self.needs_semantics else 'Không'}")
        if self.evidence:
            lines.append(f"Bằng chứng: {', '.join(self.evidence)}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Detection logic
# ---------------------------------------------------------------------------

def _detect_flutter(page) -> Optional[WebTech]:
    """Phát hiện Flutter Web và xác định renderer."""
    evidence = []

    has_flutter_view = page.locator("flutter-view").count() > 0
    has_flt_glass = page.locator("flt-glass-pane").count() > 0
    has_flt_scene = page.locator("flt-scene").count() > 0
    has_bootstrap = page.evaluate("typeof _flutter !== 'undefined' || !!document.querySelector('script[src*=\"flutter\"]')")

    if has_flutter_view:
        evidence.append("<flutter-view>")
    if has_flt_glass:
        evidence.append("<flt-glass-pane>")
    if has_flt_scene:
        evidence.append("<flt-scene>")
    if has_bootstrap:
        evidence.append("flutter_bootstrap.js")

    if not evidence:
        return None

    # Xác định renderer
    has_canvas = page.locator("canvas").count() > 0
    renderer = FlutterRenderer.CANVASKIT if has_canvas else FlutterRenderer.HTML
    if has_canvas:
        evidence.append("CanvasKit (<canvas>)")
    else:
        evidence.append("HTML renderer")

    return WebTech(
        name=TechName.FLUTTER,
        renderer=renderer,
        evidence=evidence,
    )


def _detect_react(page) -> Optional[WebTech]:
    """Phát hiện React / Next.js."""
    evidence = []
    is_react = page.evaluate("""() => {
        if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__) return 'devtools';
        if (document.querySelector('[data-reactroot]')) return 'reactroot';
        if (document.querySelector('#__next')) return 'nextjs';
        const el = document.querySelector('body > div');
        if (el && el._reactRootContainer) return 'rootContainer';
        return null;
    }""")

    if not is_react:
        return None

    is_nextjs = page.evaluate("!!document.querySelector('#__next') || !!window.__NEXT_DATA__")
    if is_nextjs:
        evidence.append("__NEXT_DATA__ / #__next")
        version = page.evaluate("window.__NEXT_DATA__?.buildId || null")
        return WebTech(name=TechName.NEXTJS, version=version, evidence=evidence)

    evidence.append(f"React detected via: {is_react}")
    return WebTech(name=TechName.REACT, evidence=evidence)


def _detect_angular(page) -> Optional[WebTech]:
    """Phát hiện Angular."""
    evidence = []
    is_angular = page.evaluate("""() => {
        if (window.ng) return 'ng';
        if (document.querySelector('[ng-version]')) return 'ng-version';
        if (document.querySelector('app-root')) return 'app-root';
        if (document.querySelector('[_nghost]') || document.querySelector('[_ngcontent]')) return 'ngcontent';
        return null;
    }""")

    if not is_angular:
        return None

    version = page.evaluate("document.querySelector('[ng-version]')?.getAttribute('ng-version') || null")
    evidence.append(f"Angular detected via: {is_angular}")
    return WebTech(name=TechName.ANGULAR, version=version, evidence=evidence)


def _detect_vue(page) -> Optional[WebTech]:
    """Phát hiện Vue.js / Nuxt.js."""
    evidence = []
    is_vue = page.evaluate("""() => {
        if (window.__VUE__) return 'vue3';
        if (window.Vue) return 'vue2';
        if (document.querySelector('[data-v-]') || document.querySelector('[data-v-app]')) return 'data-v';
        if (document.querySelector('#__nuxt') || window.__NUXT__) return 'nuxt';
        return null;
    }""")

    if not is_vue:
        return None

    is_nuxt = page.evaluate("!!document.querySelector('#__nuxt') || !!window.__NUXT__")
    if is_nuxt:
        evidence.append("__NUXT__ / #__nuxt")
        return WebTech(name=TechName.NUXTJS, evidence=evidence)

    evidence.append(f"Vue detected via: {is_vue}")
    return WebTech(name=TechName.VUE, evidence=evidence)


def _detect_svelte(page) -> Optional[WebTech]:
    """Phát hiện Svelte / SvelteKit."""
    is_svelte = page.evaluate("""() => {
        const els = document.querySelectorAll('[class]');
        for (const el of els) {
            for (const cls of el.classList) {
                if (cls.startsWith('svelte-')) return true;
            }
        }
        return !!document.querySelector('[data-sveltekit]') || !!window.__sveltekit;
    }""")
    if not is_svelte:
        return None
    return WebTech(name=TechName.SVELTE, evidence=["svelte- class prefix"])


def detect_technology(page) -> WebTech:
    """
    Phát hiện công nghệ web của trang hiện tại.

    Args:
        page: Playwright Page object (đã navigate tới URL)

    Returns:
        WebTech chứa thông tin công nghệ phát hiện được
    """
    # Thứ tự ưu tiên: Flutter trước (vì DOM đặc biệt nhất)
    detectors = [
        _detect_flutter,
        _detect_angular,  # Angular trước React (tránh false positive từ devtools hook)
        _detect_vue,
        _detect_svelte,
        _detect_react,
    ]

    for detector in detectors:
        try:
            result = detector(page)
            if result:
                return result
        except Exception:
            continue

    # Fallback: kiểm tra có phải HTML thuần
    has_forms = page.locator("form").count() > 0
    has_inputs = page.locator("input, textarea, select").count() > 0
    if has_forms or has_inputs:
        return WebTech(name=TechName.STATIC_HTML, evidence=["Standard HTML form elements"])

    return WebTech(name=TechName.UNKNOWN)


# ---------------------------------------------------------------------------
# So sánh chiến lược test automation giữa các công nghệ
# ---------------------------------------------------------------------------

COMPARISON = """
╔══════════════════════════════════════════════════════════════════════════════════╗
║              SO SÁNH TEST AUTOMATION: Flutter Web vs HTML thường               ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║  ┌─────────────────┬──────────────────────────┬─────────────────────────────┐   ║
║  │    Tiêu chí     │      HTML thường /       │      Flutter Web            │   ║
║  │                 │   React / Angular / Vue  │    (CanvasKit renderer)     │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ Rendering       │ DOM-based                │ Canvas (vẽ pixel)           │   ║
║  │                 │ Mỗi element = 1 DOM node │ Toàn bộ UI = 1 <canvas>    │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ DOM Elements    │ ✅ <input>, <button>,    │ ❌ Không có HTML elements   │   ║
║  │                 │    <div>, <a>, ...        │    nào trong DOM mặc định   │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ CSS Selectors   │ ✅ Hoạt động bình thường │ ❌ Không dùng được          │   ║
║  │                 │    #id, .class, tag       │    (không có element)       │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ XPath           │ ✅ Hoạt động             │ ❌ Không dùng được          │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ Cách tương tác  │ page.fill('input', val)  │ 1. Bật Semantics           │   ║
║  │ input           │ page.click('button')     │ 2. Tìm qua aria-label      │   ║
║  │                 │                          │ 3. Fill qua flt-editing     │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ Cách click      │ page.click('#btn')       │ Click flt-semantics có     │   ║
║  │ button          │ page.click('text=Login') │ role="button"              │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ Thời gian chờ   │ wait_for_selector        │ Cần sleep + wait vì        │   ║
║  │                 │ wait_for_load_state      │ Flutter render async        │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ Screenshot      │ ✅ Chụp được bình thường │ ✅ Chụp được (canvas)      │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ Text assertion  │ page.content() chứa text │ Text chỉ hiện trong        │   ║
║  │                 │                          │ semantics (nếu bật)        │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ Inspect element │ ✅ DevTools Elements tab  │ ⚠️ Chỉ thấy <canvas>     │   ║
║  │ (DevTools)      │    hiện full DOM tree     │    Cần bật semantics       │   ║
║  ├─────────────────┼──────────────────────────┼─────────────────────────────┤   ║
║  │ Tốc độ test     │ Nhanh                    │ Chậm hơn (cần thời gian    │   ║
║  │                 │                          │ render canvas + semantics)  │   ║
║  └─────────────────┴──────────────────────────┴─────────────────────────────┘   ║
║                                                                                ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""


def print_comparison():
    """In bảng so sánh ra console."""
    print(COMPARISON)


# ---------------------------------------------------------------------------
# CLI: chạy trực tiếp để phát hiện công nghệ của một URL
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    from playwright.sync_api import sync_playwright

    url = sys.argv[1] if len(sys.argv) > 1 else "https://stqa.rbc.vn"

    print(f"\n🔍 Đang phân tích: {url}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        time.sleep(2)

        tech = detect_technology(page)
        print(tech.summary())

        if tech.is_flutter:
            print("\n⚠️  Đây là Flutter Web — cần chiến lược test đặc biệt!")
            print("   Xem conftest.py để biết cách sử dụng helper functions.")
        else:
            print("\n✅ Trang dùng DOM tiêu chuẩn — có thể dùng CSS selector bình thường.")

        print_comparison()
        browser.close()
