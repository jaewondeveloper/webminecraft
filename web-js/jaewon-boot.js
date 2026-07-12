"use strict";
window.__eaglerSplash2URL = window.__eaglerSplash2URL || "splash2.png?v=23";
window.__eaglerClassesJSURL = window.__eaglerClassesJSURL || null;

var __eaglerEarlySplashSelectors = [
	"._eaglercraftX_early_splash_element"
];

function __eaglerHideNodes(selectors) {
	for (var i = 0; i < selectors.length; i++) {
		var nodes = document.querySelectorAll(selectors[i]);
		for (var j = 0; j < nodes.length; j++) {
			nodes[j].setAttribute("data-eagler-overlay-hidden", "1");
			nodes[j].style.setProperty("display", "none", "important");
			nodes[j].style.setProperty("visibility", "hidden", "important");
		}
	}
}

function __eaglerRestoreOverlayHidden() {
	var nodes = document.querySelectorAll("[data-eagler-overlay-hidden]");
	for (var i = 0; i < nodes.length; i++) {
		nodes[i].style.removeProperty("display");
		nodes[i].style.removeProperty("visibility");
		nodes[i].removeAttribute("data-eagler-overlay-hidden");
	}
}

function __eaglerHideBootScreens() {
	var boot = document.getElementById("launch_countdown_screen");
	if (boot) {
		boot.style.setProperty("display", "none", "important");
		boot.style.setProperty("visibility", "hidden", "important");
	}
	__eaglerHideNodes(__eaglerEarlySplashSelectors);
}

function __eaglerEnsureOverlayHost() {
	return document.body || document.documentElement;
}

window.__eaglerSetLoadingStatus = function(msg) {
	window.__eaglerLastStatusText = msg;
	window.__eaglerLastStatusAt = performance.now();
	var state = window.__eaglerOverlayState;
	if (state && state.statusEl) {
		state.statusEl.textContent = msg;
	}
};

window.__eaglerSetLoadingProgress = function(pct) {
	var state = window.__eaglerOverlayState;
	if (!state || !state.inner) return;
	var p = Math.max(0, Math.min(0.95, pct / 100));
	state.inner.style.width = (p * 100) + "%";
	state.manualProgress = true;
};

window.__eaglerInstallNetworkStatusHooks = function() {
	if (window.__eaglerNetworkHooksInstalled) return;
	window.__eaglerNetworkHooksInstalled = true;

	function labelFromUrl(url) {
		if (!url) return "파일";
		var s = String(url);
		if (s.indexOf("classes.js") !== -1) return "게임 엔진 (classes.js)";
		if (s.indexOf("assets.epk") !== -1) return "에셋 패키지 (assets.epk)";
		if (s.indexOf("splash") !== -1) return "이미지";
		var slash = s.lastIndexOf("/");
		return slash >= 0 ? s.slice(slash + 1) : s;
	}

	if (typeof window.fetch === "function") {
		var origFetch = window.fetch;
		window.fetch = function(input, init) {
			var url = (typeof input === "string") ? input : (input && input.url) ? input.url : "";
			if (url && url.indexOf("http") === 0 || url.indexOf("/") === 0 || url.indexOf("assets") !== -1) {
				window.__eaglerSetLoadingStatus(labelFromUrl(url) + " 다운로드 중...");
			}
			return origFetch.apply(this, arguments).then(function(res) {
				if (url) window.__eaglerSetLoadingStatus(labelFromUrl(url) + " 처리 중...");
				return res;
			});
		};
	}

	var XO = window.XMLHttpRequest;
	if (XO && XO.prototype) {
		var origOpen = XO.prototype.open;
		var origSend = XO.prototype.send;
		XO.prototype.open = function(method, url) {
			this.__eaglerUrl = url;
			return origOpen.apply(this, arguments);
		};
		XO.prototype.send = function() {
			var self = this;
			var url = self.__eaglerUrl || "";
			if (url) {
				window.__eaglerSetLoadingStatus(labelFromUrl(url) + " 다운로드 중...");
				self.addEventListener("progress", function(ev) {
					if (ev.lengthComputable && ev.total > 0) {
						var pct = (ev.loaded / ev.total) * 100;
						window.__eaglerSetLoadingProgress(pct);
						window.__eaglerSetLoadingStatus(
							labelFromUrl(url) + " 다운로드 중... " + Math.floor(pct) + "%"
						);
					}
				});
				self.addEventListener("loadend", function() {
					if (self.status >= 200 && self.status < 400) {
						window.__eaglerSetLoadingStatus(labelFromUrl(url) + " 완료");
					}
				});
			}
			return origSend.apply(this, arguments);
		};
	}
};

window.__eaglerLoadTextWithProgress = function(url, label, onLoad, onError) {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", url, true);
	xhr.responseType = "text";
	xhr.addEventListener("progress", function(ev) {
		if (ev.lengthComputable && ev.total > 0) {
			var pct = (ev.loaded / ev.total) * 100;
			window.__eaglerSetLoadingProgress(pct);
			window.__eaglerSetLoadingStatus(label + " 다운로드 중... " + Math.floor(pct) + "%");
		} else {
			window.__eaglerSetLoadingStatus(label + " 다운로드 중... " + Math.floor(ev.loaded / 1024) + " KB");
		}
	});
	xhr.addEventListener("load", function() {
		if (xhr.status >= 200 && xhr.status < 300) {
			window.__eaglerSetLoadingStatus(label + " 설치 중...");
			onLoad(xhr.responseText);
		} else if (onError) {
			onError(new Error("HTTP " + xhr.status));
		}
	});
	xhr.addEventListener("error", function() {
		if (onError) onError(new Error("network error"));
	});
	xhr.send();
};

window.__eaglerEnsureClassesLoaded = function(callback) {
	if (typeof main === "function") {
		callback();
		return;
	}
	var url = window.__eaglerClassesJSURL;
	if (!url) {
		alert("classes.js URL 없음");
		return;
	}
	window.__eaglerShowLoadingSplashAfterMain();
	window.__eaglerInstallNetworkStatusHooks();
	window.__eaglerSetLoadingStatus("게임 엔진 다운로드 준비...");
	window.__eaglerLoadTextWithProgress(url, "게임 엔진", function(src) {
		src = String(src).replace(/^\uFEFF/, "").replace(/\s*<\/script>\s*$/i, "").trim();
		if (!src || src.charAt(0) === "<") {
			alert("classes.js 다운로드 실패: HTML 응답 (404 또는 서버 오류)");
			return;
		}
		var s = document.createElement("script");
		s.type = "text/javascript";
		s.text = src;
		window.eaglercraftXClientScriptElement = s;
		document.head.appendChild(s);
		window.__eaglerSetLoadingStatus("게임 엔진 초기화 중...");
		setTimeout(function() {
			if (typeof main === "function") callback();
			else alert("classes.js 로드 후 main() 없음");
		}, 100);
	}, function(err) {
		alert("classes.js 다운로드 실패: " + err.message);
	});
};

window.__eaglerShowLoadingSplash = function(wrapper) {
	var host = __eaglerEnsureOverlayHost();
	if (!host) return;

	var img = window.__eaglerSplash2URL || "splash2.png?v=23";
	var minMs = (typeof window.__eaglerOverlayMinMs === "number") ? window.__eaglerOverlayMinMs : 12000;
	var useTimerOnly = window.__eaglerOverlayMode === "timer";
	var showStatus = window.__eaglerShowLoadingStatus !== false;
	var state = window.__eaglerOverlayState;
	var overlay, inner, statusEl, start, dismissed, mojangSeen, titleStable, glErrors;

	if (state && state.overlay && state.overlay.parentNode) {
		overlay = state.overlay;
		inner = state.inner;
		statusEl = state.statusEl;
		start = state.start;
		dismissed = state.dismissed();
		mojangSeen = state.mojangSeen || false;
		titleStable = state.titleStable || 0;
		glErrors = state.glErrors || 0;
		if (overlay.parentNode !== host) host.appendChild(overlay);
		state.wrapper = wrapper || document.querySelector("._eaglercraftX_wrapper_element");
		if (statusEl && window.__eaglerLastStatusText) statusEl.textContent = window.__eaglerLastStatusText;
		return;
	}

	overlay = document.createElement("div");
	overlay.className = "_eaglercraftX_loading_overlay";
	overlay.style.cssText = "position:fixed;top:0;left:0;right:0;bottom:0;z-index:2147483646;pointer-events:none;image-rendering:pixelated;background:center / contain no-repeat url(\"" + img + "\"), 0px 0px / 1000000% 1000000% no-repeat url(\"" + img + "\") black";
	var barHost = document.createElement("div");
	barHost.className = "_eaglercraftX_loading_bar_host";
	barHost.style.cssText = "position:absolute;left:50%;top:72%;transform:translateX(-50%);width:min(640px,88vw);pointer-events:none;";
	var outer = document.createElement("div");
	outer.style.cssText = "box-sizing:border-box;height:20px;padding:2px;border:2px solid #ffffff;background:transparent;";
	inner = document.createElement("div");
	inner.style.cssText = "height:100%;width:0%;background:#ffffff;box-sizing:border-box;";
	outer.appendChild(inner);
	barHost.appendChild(outer);
	overlay.appendChild(barHost);
	if (showStatus) {
		statusEl = document.createElement("div");
		statusEl.className = "_eaglercraftX_loading_status";
		statusEl.style.cssText = "position:absolute;left:50%;top:78%;transform:translateX(-50%);width:min(640px,92vw);color:#ffffff;font:15px/1.4 sans-serif;text-align:center;text-shadow:0 0 6px #000,0 0 2px #000;pointer-events:none;";
		statusEl.textContent = window.__eaglerLastStatusText || "로딩 중...";
		overlay.appendChild(statusEl);
	}
	host.appendChild(overlay);

	start = performance.now();
	mojangSeen = false;
	titleStable = 0;
	dismissed = false;
	glErrors = 0;

	var idleMessages = [
		"에셋 패키지 읽는 중...",
		"리소스 준비 중...",
		"월드 데이터 초기화 중...",
		"그래픽 엔진 준비 중...",
		"거의 다 됐습니다..."
	];

	state = {
		wrapper: wrapper || null,
		overlay: overlay,
		inner: inner,
		statusEl: statusEl || null,
		start: start,
		mojangSeen: false,
		titleStable: 0,
		glErrors: 0,
		manualProgress: false,
		dismissed: function() { return dismissed; },
		markDismissed: function() { dismissed = true; }
	};
	window.__eaglerOverlayState = state;
	__eaglerHideBootScreens();

	function __eaglerHideGameBootDuringOverlay() {
		__eaglerHideNodes(__eaglerEarlySplashSelectors);
	}

	function sampleGameScreen() {
		var root = state.wrapper || document.querySelector("._eaglercraftX_wrapper_element");
		if (!root) return null;
		var canvas = root.querySelector("._eaglercraftX_canvas_element");
		if (!canvas || canvas.width < 16 || canvas.height < 16) return null;
		var gl = null;
		try {
			gl = canvas.getContext("webgl2") || canvas.getContext("webgl");
		} catch (e) {
			glErrors++;
			state.glErrors = glErrors;
			return null;
		}
		if (!gl || gl.isContextLost && gl.isContextLost()) {
			glErrors++;
			state.glErrors = glErrors;
			return null;
		}
		var w = canvas.width, h = canvas.height, px = new Uint8Array(4);
		var corners = [], centers = [];
		var pts = [[0.06, 0.06], [0.94, 0.06], [0.06, 0.94], [0.94, 0.94], [0.5, 0.5], [0.5, 0.38]];
		for (var i = 0; i < pts.length; i++) {
			var x = Math.max(0, Math.min(w - 1, (pts[i][0] * w) | 0));
			var y = Math.max(0, Math.min(h - 1, (pts[i][1] * h) | 0));
			try {
				gl.readPixels(x, h - y - 1, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
			} catch (e) {
				glErrors++;
				state.glErrors = glErrors;
				return null;
			}
			if (gl.getError && gl.getError() !== 0) {
				glErrors++;
				state.glErrors = glErrors;
				return null;
			}
			var s = { r: px[0], g: px[1], b: px[2] };
			if (i < 4) corners.push(s); else centers.push(s);
		}
		var cornerAvg = 0;
		for (var j = 0; j < corners.length; j++) cornerAvg += (corners[j].r + corners[j].g + corners[j].b) / 3;
		cornerAvg /= corners.length;
		var whiteCorners = 0;
		for (var k = 0; k < corners.length; k++) {
			if (corners[k].r > 205 && corners[k].g > 205 && corners[k].b > 205) whiteCorners++;
		}
		var centerRed = false;
		for (var m = 0; m < centers.length; m++) {
			if (centers[m].r > 110 && centers[m].g < 95 && centers[m].b < 95) centerRed = true;
		}
		return {
			cornerAvg: cornerAvg,
			whiteCorners: whiteCorners,
			centerRed: centerRed,
			isMojang: whiteCorners >= 3 && cornerAvg > 215,
			isTitle: whiteCorners <= 1 && cornerAvg < 155
		};
	}

	function dismissOverlay() {
		if (dismissed) return;
		dismissed = true;
		state.markDismissed();
		inner.style.width = "100%";
		if (statusEl) statusEl.textContent = "완료!";
		setTimeout(function() {
			if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
			if (window.__eaglerOverlayState && window.__eaglerOverlayState.overlay === overlay) {
				window.__eaglerOverlayState = null;
			}
			__eaglerRestoreOverlayHidden();
		}, 120);
	}

	function poll() {
		if (dismissed) return;
		var elapsed = performance.now() - start;
		if (!state.manualProgress) {
			var barTarget = Math.min(0.92, elapsed / Math.max(minMs, 8000));
			inner.style.width = (barTarget * 100) + "%";
		}
		if (!state.wrapper) {
			state.wrapper = document.querySelector("._eaglercraftX_wrapper_element");
		}
		if (overlay.parentNode !== host) host.appendChild(overlay);
		__eaglerHideGameBootDuringOverlay();

		if (showStatus && statusEl) {
			var stale = performance.now() - (window.__eaglerLastStatusAt || 0);
			var base = window.__eaglerLastStatusText || "로딩 중...";
			if (stale > 3500 && !state.manualProgress) {
				var idx = Math.floor(elapsed / 3500) % idleMessages.length;
				base = idleMessages[idx];
			}
			var sec = Math.floor(elapsed / 1000);
			statusEl.textContent = sec > 0 ? (base + " (" + sec + "초)") : base;
		}

		if (useTimerOnly) {
			if (elapsed >= minMs) {
				dismissOverlay();
				return;
			}
		} else if (elapsed >= 8000) {
			var sample = sampleGameScreen();
			if (sample) {
				if (sample.isMojang || (sample.whiteCorners >= 2 && sample.centerRed)) {
					mojangSeen = true;
					state.mojangSeen = true;
				}
				if (mojangSeen && sample.isTitle) {
					titleStable++;
					state.titleStable = titleStable;
					if (titleStable >= 4) { dismissOverlay(); return; }
				} else if (mojangSeen && !sample.isMojang && sample.cornerAvg < 170) {
					titleStable++;
					state.titleStable = titleStable;
					if (titleStable >= 3) { dismissOverlay(); return; }
				} else {
					titleStable = 0;
					state.titleStable = 0;
				}
			}
		}
		if (elapsed > 120000) { dismissOverlay(); return; }
		setTimeout(poll, useTimerOnly ? 200 : 250);
	}
	poll();
};

window.__eaglerShowLoadingSplashAfterMain = function() {
	if (typeof window.__eaglerShowLoadingSplash === "function") {
		window.__eaglerShowLoadingSplash(null);
	}
};

window.__eaglerStartLoadingOverlayWatch = function() {
	if (window.__eaglerOverlayWatchStarted) return;
	window.__eaglerOverlayWatchStarted = true;
	var waitWrapper = setInterval(function() {
		if (window.__eaglerOverlayState && window.__eaglerOverlayState.dismissed()) {
			clearInterval(waitWrapper);
			return;
		}
		var wrapper = document.querySelector("._eaglercraftX_wrapper_element");
		if (wrapper && window.__eaglerOverlayState) {
			window.__eaglerOverlayState.wrapper = wrapper;
		}
	}, 100);
	setTimeout(function() { clearInterval(waitWrapper); }, 120000);
};

// 8084: 페이지 셸 로드 완료 표시
window.addEventListener("load", function() {
	if (window.__eaglerClassesJSURL && typeof main !== "function") {
		if (typeof window.__eaglerSetLoadingStatus === "function") {
			window.__eaglerSetLoadingStatus("준비 완료 — 아무 키나 누르세요");
		}
	}
});
