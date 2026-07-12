(function() {
	"use strict";

	var STORAGE_KEY = "minecraftLauncherSettings";
	var INSTALL_STORAGE_KEY = "minecraftLauncherInstalled";
	var LAUNCHER_VERSION = 4;
	var CREEPER_ICON = "creeper.jpg";
	var DEFAULT_INSTALLED = ["wasm-1122"];

	var ID_MIGRATION = {
		"wasm-120": "wasm-1122",
		"js-120": "js-1122",
		"mod-120a": "mod-eagly-js",
		"mod-120b": "mod-eagly-wasm",
		"mod-120c": "mod-chrome",
		"snap-120": "snap-1122",
		"beta-119": "beta-188"
	};

	var CATALOG = [
		{ id: "wasm-1122", name: "Minecraft", subtitle: "Latest release · WASM", edition: "web", folder: "web", port: 8080, version: "1.12.2", engine: "WASM", latest: true, size: "142 MB" },
		{ id: "js-1122", name: "Minecraft", subtitle: "Latest release · JavaScript", edition: "web", folder: "web-js", port: 8084, version: "1.12.2", engine: "JavaScript", size: "198 MB" },
		{ id: "mod-eagly-js", name: "Minecraft", subtitle: "EaglyMC · Modded 1.8.8", edition: "mod", folder: "eaglymc", port: 8081, version: "1.8.8", engine: "Mod JS", size: "156 MB" },
		{ id: "mod-eagly-wasm", name: "Minecraft", subtitle: "EaglyMC · Modded WASM", edition: "mod", folder: "eaglymc-wasm", port: 8082, version: "1.8.8", engine: "Mod WASM", size: "161 MB" },
		{ id: "mod-chrome", name: "Minecraft", subtitle: "EaglyMC · 저사양 1.8.8", edition: "mod", folder: "eaglymc-chromebook", port: 8083, version: "1.8.8", engine: "Chromebook", size: "148 MB" },
		{ id: "astra-1192", name: "Minecraft", subtitle: "Astra Edition · 리소스팩", edition: "mod", folder: "minecraft-astra", port: 8085, version: "1.19.2", engine: "Astra", size: "214 MB" },
		{ id: "snap-1122", name: "Minecraft", subtitle: "Snapshot · 17w50a", edition: "web", folder: "web-js", port: 8084, version: "1.12.2", engine: "Snapshot", snapshot: true, size: "201 MB" },
		{ id: "beta-188", name: "Minecraft", subtitle: "Beta · 1.8.8", edition: "web", folder: "eaglymc", port: 8081, version: "1.8.8", engine: "Beta", size: "138 MB" },
		{ id: "legacy-152", name: "Minecraft", subtitle: "Classic · 1.5.2", edition: "web", folder: "eaglymc-wasm", port: 8082, version: "1.5.2", engine: "Legacy", size: "95 MB" },
		{ id: "release-188-wasm", name: "Minecraft", subtitle: "Release · 1.8.8 WASM", edition: "web", folder: "eaglymc-wasm", port: 8082, version: "1.8.8", engine: "WASM", size: "120 MB" }
	];

	var state = {
		settings: loadSettings(),
		selectedId: null,
		status: {},
		modalResolve: null
	};

	function defaultSettings() {
		return {
			username: "Gigabit1019855",
			defaultVersionId: "wasm-1122",
			fullscreenLaunch: true,
			showGiftBanner: true,
			reduceMotion: false,
			installedVersions: DEFAULT_INSTALLED.slice(),
			launcherVersion: LAUNCHER_VERSION
		};
	}

	function loadDedicatedInstalled() {
		try {
			var raw = localStorage.getItem(INSTALL_STORAGE_KEY);
			if (!raw) return null;
			var list = JSON.parse(raw);
			return Array.isArray(list) ? list : null;
		} catch (e) {
			return null;
		}
	}

	function migrateVersionIds(s) {
		if (s.installedVersions && s.installedVersions.length) {
			s.installedVersions = s.installedVersions.map(function(id) {
				return ID_MIGRATION[id] || id;
			}).filter(function(id, idx, arr) { return arr.indexOf(id) === idx; });
		}
		if (ID_MIGRATION[s.defaultVersionId]) {
			s.defaultVersionId = ID_MIGRATION[s.defaultVersionId];
		}
		return s;
	}

	function loadSettings() {
		try {
			var raw = localStorage.getItem(STORAGE_KEY);
			if (raw) {
				var s = Object.assign(defaultSettings(), JSON.parse(raw));
				s = migrateVersionIds(s);
				var dedicated = loadDedicatedInstalled();
				if (dedicated && dedicated.length) {
					s.installedVersions = migrateVersionIds({ installedVersions: dedicated }).installedVersions;
				}
				if (!s.installedVersions || !s.installedVersions.length) {
					s.installedVersions = DEFAULT_INSTALLED.slice();
				}
				if (!s.launcherVersion) {
					s.launcherVersion = LAUNCHER_VERSION;
				} else if (s.launcherVersion < LAUNCHER_VERSION) {
					s.launcherVersion = LAUNCHER_VERSION;
				}
				return s;
			}
		} catch (e) {}
		var dedicatedDefault = loadDedicatedInstalled();
		if (dedicatedDefault && dedicatedDefault.length) {
			var migrated = migrateVersionIds({ installedVersions: dedicatedDefault, defaultVersionId: "wasm-1122" });
			var base = defaultSettings();
			base.installedVersions = migrated.installedVersions;
			base.launcherVersion = LAUNCHER_VERSION;
			return base;
		}
		return defaultSettings();
	}

	function saveInstalledVersions() {
		localStorage.setItem(INSTALL_STORAGE_KEY, JSON.stringify(state.settings.installedVersions));
	}

	function saveSettings() {
		saveInstalledVersions();
		localStorage.setItem(STORAGE_KEY, JSON.stringify(state.settings));
	}

	function $(sel) { return document.querySelector(sel); }
	function $all(sel) { return document.querySelectorAll(sel); }

	function isInstalled(id) {
		return state.settings.installedVersions.indexOf(id) !== -1;
	}

	function installedCatalog() {
		return CATALOG.filter(function(v) { return isInstalled(v.id); });
	}

	function getVersion(id) {
		for (var i = 0; i < CATALOG.length; i++) {
			if (CATALOG[i].id === id) return CATALOG[i];
		}
		return CATALOG[0];
	}

	function selectedVersion() {
		var id = state.selectedId || state.settings.defaultVersionId;
		if (!isInstalled(id)) {
			id = state.settings.installedVersions[0] || "wasm-1122";
		}
		return getVersion(id);
	}

	function editionLabel(edition) {
		return edition === "web" ? "Web Edition" : "Mod Edition";
	}

	function versionIconHtml() {
		return '<img class="version-icon-img" src="' + CREEPER_ICON + '" alt="">';
	}

	function isLocalDev() {
		var host = window.location.hostname;
		return host === "localhost" || host === "127.0.0.1";
	}

	function siteBasePath() {
		var path = window.location.pathname || "/";
		if (/\/index\.html$/i.test(path)) path = path.replace(/\/index\.html$/i, "");
		if (path.length > 1 && path.charAt(path.length - 1) === "/") path = path.slice(0, -1);
		return path;
	}

	function gameUrl(version) {
		var folder = version.folder || "web";
		if (isLocalDev() && version.port) {
			return "http://localhost:" + version.port + "/";
		}
		return window.location.origin + siteBasePath() + "/" + folder + "/";
	}

	function probeServer(version) {
		return new Promise(function(resolve) {
			var settled = false;
			function done(ok) {
				if (settled) return;
				settled = true;
				resolve(ok);
			}
			var img = new Image();
			img.onload = function() { done(true); };
			img.onerror = function() {
				fetch(gameUrl(version), { mode: "no-cors", cache: "no-store" })
					.then(function() { done(true); })
					.catch(function() { done(false); });
			};
			setTimeout(function() { done(false); }, 5000);
			img.src = gameUrl(version) + "favicon.png?_=" + Date.now();
		});
	}

	function applyMotionPref() {
		document.body.classList.toggle("no-motion", !!state.settings.reduceMotion);
	}

	function showToast(msg) {
		var t = $("#launch-toast");
		if (!t) return;
		t.textContent = msg;
		t.classList.add("show");
		setTimeout(function() { t.classList.remove("show"); }, 2800);
	}

	/* ── Custom modal (mc-button) ── */
	function closeModal(result) {
		var root = $("#mc-modal");
		if (!root) return;
		root.classList.remove("open");
		var resolve = state.modalResolve;
		state.modalResolve = null;
		if (resolve) resolve(result);
	}

	function showModal(opts) {
		opts = opts || {};
		return new Promise(function(resolve) {
			state.modalResolve = resolve;
			var root = $("#mc-modal");
			var title = $("#mc-modal-title");
			var body = $("#mc-modal-body");
			var actions = $("#mc-modal-actions");
			var progress = $("#mc-modal-progress-wrap");
			var progressInner = $("#mc-modal-progress-inner");
			var progressLabel = $("#mc-modal-progress-label");

			if (title) title.textContent = opts.title || "Minecraft Launcher";
			if (body) body.textContent = opts.message || "";

			if (progress) progress.style.display = opts.progress ? "block" : "none";
			if (progressInner) progressInner.style.width = (opts.progressPct || 0) + "%";
			if (progressLabel) {
				progressLabel.style.display = opts.progress ? "block" : "none";
				progressLabel.textContent = opts.progressText || "";
			}

			if (actions) {
				actions.innerHTML = "";
				var buttons = opts.buttons || [];
				if (!buttons.length && opts.confirm) {
					buttons = [
						{ label: "취소", variant: "gray", value: false },
						{ label: "확인", variant: "green", value: true }
					];
				}
				if (!buttons.length) {
					buttons = [{ label: "확인", variant: "green", value: true }];
				}
				buttons.forEach(function(b) {
					var btn = document.createElement("mc-button");
					btn.setAttribute("width", b.width || "120px");
					btn.setAttribute("height", "40px");
					if (b.variant === "gray") {
						btn.setAttribute("bg-top", "#5a5a5a");
						btn.setAttribute("bg-bottom", "#3a3a3a");
					} else if (b.variant === "red") {
						btn.setAttribute("bg-top", "#c43c3c");
						btn.setAttribute("bg-bottom", "#8b2020");
					} else {
						btn.setAttribute("bg-top", "#1cb853");
						btn.setAttribute("bg-bottom", "#0f8b3e");
					}
					btn.textContent = b.label;
					btn.addEventListener("click", function() {
						closeModal(b.value !== undefined ? b.value : b.label);
					});
					actions.appendChild(btn);
				});
			}

			root.classList.add("open");
		});
	}

	function showConfirm(title, message) {
		return showModal({
			title: title,
			message: message,
			buttons: [
				{ label: "취소", variant: "gray", value: false },
				{ label: "확인", variant: "green", value: true }
			]
		});
	}

	function showAlert(title, message) {
		return showModal({
			title: title,
			message: message,
			buttons: [{ label: "확인", variant: "green", value: true }]
		});
	}

	function fakeInstallProgress(version) {
		return new Promise(function(resolve) {
			var pct = 0;
			var steps = [
				"다운로드 준비 중...",
				"Minecraft " + version.version + " 다운로드 중...",
				"에셋 검증 중...",
				"네이티브 라이브러리 설치 중...",
				"설치 완료!"
			];
			var step = 0;

			showModal({
				title: "버전 설치",
				message: "Minecraft " + version.version + "\n" + version.subtitle,
				progress: true,
				progressPct: 0,
				progressText: steps[0],
				buttons: []
			});

			var root = $("#mc-modal");
			root.classList.add("open");

			var timer = setInterval(function() {
				pct += Math.random() * 12 + 4;
				if (pct >= 100) {
					pct = 100;
					clearInterval(timer);
					var inner = $("#mc-modal-progress-inner");
					var label = $("#mc-modal-progress-label");
					if (inner) inner.style.width = "100%";
					if (label) label.textContent = steps[4];
					setTimeout(function() {
						closeModal(true);
						resolve(true);
					}, 500);
					return;
				}
				var inner = $("#mc-modal-progress-inner");
				var label = $("#mc-modal-progress-label");
				if (inner) inner.style.width = Math.floor(pct) + "%";
				var newStep = Math.min(steps.length - 2, Math.floor(pct / 25));
				if (newStep !== step) {
					step = newStep;
					if (label) label.textContent = steps[step];
				}
			}, 180);
		});
	}

	function installVersion(id) {
		var v = getVersion(id);
		if (isInstalled(id)) {
			showToast("이미 설치된 버전입니다.");
			return;
		}
		fakeInstallProgress(v).then(function() {
			state.settings.installedVersions.push(id);
			if (state.settings.installedVersions.length === 1) {
				state.settings.defaultVersionId = id;
			}
			saveSettings();
			renderAllLists();
			renderInstallManager();
			showToast("Minecraft " + v.version + " 설치 완료");
		});
	}

	function uninstallVersion(id) {
		var v = getVersion(id);
		if (!isInstalled(id)) return;
		if (state.settings.installedVersions.length <= 1) {
			showAlert("삭제 불가", "최소 하나의 버전은 설치되어 있어야 합니다.");
			return;
		}
		showConfirm("버전 삭제", "Minecraft " + v.version + " (" + v.subtitle + ")\n\n이 버전을 삭제하시겠습니까?").then(function(ok) {
			if (!ok) return;
			state.settings.installedVersions = state.settings.installedVersions.filter(function(x) { return x !== id; });
			if (state.settings.defaultVersionId === id) {
				state.settings.defaultVersionId = state.settings.installedVersions[0];
			}
			if (state.selectedId === id) {
				state.selectedId = state.settings.defaultVersionId;
			}
			saveSettings();
			renderAllLists();
			renderInstallManager();
			updateSelectedUI();
			showToast("Minecraft " + v.version + " 삭제됨");
		});
	}

	function renderVersionCards(container, list) {
		if (!container) return;
		container.innerHTML = "";
		if (!list.length) {
			container.innerHTML = '<div class="empty-state">설치된 버전이 없습니다.<br>설정 → 버전 설치에서 추가하세요.</div>';
			return;
		}
		list.forEach(function(v) {
			var card = document.createElement("div");
			card.className = "version-card" + (state.selectedId === v.id ? " selected" : "");
			card.setAttribute("data-version-id", v.id);
			var online = state.status[v.id] === true;
			var latestTag = v.latest ? '<span class="install-badge on" style="margin-left:6px">최신</span>' : "";
			card.innerHTML =
				'<div class="version-card-top">' +
					versionIconHtml() +
					'<div class="version-meta">' +
						'<div class="version-name">' + v.name + " " + v.version + latestTag + '</div>' +
						'<div class="version-sub">' + v.subtitle + '</div>' +
					'</div>' +
					'<span class="status-pill ' + (online ? "online" : (state.status[v.id] === false ? "offline" : "checking")) + '">' + (online ? "준비됨" : (state.status[v.id] === false ? "오프라인" : "확인 중")) + '</span>' +
				'</div>' +
				'<div class="version-foot">' +
					'<span>' + editionLabel(v.edition) + '</span>' +
					'<span class="mini-play-wrap" data-version="' + v.id + '"></span>' +
				'</div>';
			card.addEventListener("click", function(e) {
				if (e.target && e.target.closest && e.target.closest(".mini-play-wrap")) return;
				selectVersion(v.id);
			});
			container.appendChild(card);
			var playWrap = card.querySelector(".mini-play-wrap");
			if (playWrap) {
				var miniBtn = document.createElement("mc-button");
				miniBtn.setAttribute("width", "72px");
				miniBtn.setAttribute("height", "32px");
				miniBtn.textContent = "플레이";
				miniBtn.addEventListener("click", function(e) {
					e.stopPropagation();
					selectVersion(v.id);
					launchSelected();
				});
				playWrap.appendChild(miniBtn);
			}
		});
	}

	function renderInstallManager() {
		var list = $("#install-manager-list");
		if (!list) return;
		list.innerHTML = "";
		CATALOG.forEach(function(v, idx) {
			var row = document.createElement("div");
			var installed = isInstalled(v.id);
			row.className = "install-row" + (installed ? " installed" : "");
			row.style.animationDelay = (idx * 0.05) + "s";
			row.style.animation = "cardPop 0.4s ease backwards";
			row.innerHTML =
				'<img class="version-icon-img" src="' + CREEPER_ICON + '" alt="">' +
				'<div class="install-row-meta">' +
					'<div class="install-row-title">Minecraft ' + v.version + (v.latest ? " · 최신" : "") + '</div>' +
					'<div class="install-row-sub">' + v.subtitle + " · " + v.size + '</div>' +
				'</div>' +
				'<span class="install-badge ' + (installed ? "on" : "off") + '">' + (installed ? "설치됨" : "미설치") + '</span>' +
				'<div class="install-actions" data-id="' + v.id + '"></div>';
			var actions = row.querySelector(".install-actions");
			if (installed) {
				var unBtn = document.createElement("mc-button");
				unBtn.setAttribute("width", "88px");
				unBtn.setAttribute("height", "36px");
				unBtn.setAttribute("bg-top", "#c43c3c");
				unBtn.setAttribute("bg-bottom", "#8b2020");
				unBtn.textContent = "삭제";
				unBtn.addEventListener("click", function() { uninstallVersion(v.id); });
				actions.appendChild(unBtn);
			} else {
				var inBtn = document.createElement("mc-button");
				inBtn.setAttribute("width", "88px");
				inBtn.setAttribute("height", "36px");
				inBtn.textContent = "설치";
				inBtn.addEventListener("click", function() { installVersion(v.id); });
				actions.appendChild(inBtn);
			}
			list.appendChild(row);
		});
	}

	function updateCardSelection() {
		$all(".version-card").forEach(function(card) {
			var id = card.getAttribute("data-version-id");
			card.classList.toggle("selected", id === state.selectedId);
		});
	}

	function updateServerStatusPills() {
		$all(".version-card").forEach(function(card) {
			var id = card.getAttribute("data-version-id");
			var pill = card.querySelector(".status-pill");
			if (!pill || !id) return;
			var online = state.status[id] === true;
			var offline = state.status[id] === false;
			pill.className = "status-pill " + (online ? "online" : (offline ? "offline" : "checking"));
			pill.textContent = online ? "준비됨" : (offline ? "오프라인" : "확인 중");
		});
	}

	function selectVersion(id) {
		if (!isInstalled(id)) return;
		state.selectedId = id;
		state.settings.defaultVersionId = id;
		saveSettings();
		updateSelectedUI();
		updateCardSelection();
	}

	function updateSelectedUI() {
		var v = selectedVersion();
		var title = $("#selected-version-title");
		var number = $("#selected-version-number");
		var username = $("#right-username-label");
		if (title) title.textContent = v.name + " " + v.version;
		if (number) number.textContent = v.subtitle;
		if (username) username.textContent = state.settings.username;
		var profileName = $(".profile-info .username");
		if (profileName) profileName.textContent = state.settings.username;
		var defaultSel = $("#setting-default-version");
		if (defaultSel) defaultSel.value = v.id;
	}

	function renderAllLists() {
		var installed = installedCatalog();
		renderVersionCards($("#home-version-grid"), installed);
		renderVersionCards($("#web-version-grid"), installed.filter(function(v) { return v.edition === "web"; }));
		renderVersionCards($("#mod-version-grid"), installed.filter(function(v) { return v.edition === "mod"; }));
	}

	function checkServers() {
		CATALOG.forEach(function(v) {
			if (!isInstalled(v.id)) return;
			probeServer(v).then(function(ok) {
				state.status[v.id] = ok;
				updateServerStatusPills();
			});
		});
	}

	function launchSelected() {
		var v = selectedVersion();
		if (!isInstalled(v.id)) {
			showAlert("실행 불가", "이 버전은 설치되어 있지 않습니다.\n설정 → 버전 설치에서 설치하세요.");
			return;
		}
		var overlay = $("#game-overlay");
		var frame = $("#game-frame");
		if (!overlay || !frame) return;

		function doLaunch() {
			frame.onload = function() {
				setTimeout(focusGameFrame, 80);
				setTimeout(focusGameFrame, 400);
			};
			frame.src = gameUrl(v);
			overlay.classList.add("active");
			showToast("Minecraft " + v.version + " 실행 중...");
			setTimeout(focusGameFrame, 120);
			if (state.settings.fullscreenLaunch) {
				try {
					if (overlay.requestFullscreen) overlay.requestFullscreen();
				} catch (e) {}
			}
		}

		function focusGameFrame() {
			try {
				frame.focus();
				if (frame.contentWindow) frame.contentWindow.focus();
			} catch (e) {}
		}

		if (state.status[v.id]) {
			doLaunch();
			return;
		}
		probeServer(v).then(function(ok) {
			state.status[v.id] = ok;
			updateServerStatusPills();
			if (!ok) {
				showAlert("서버 오프라인", "게임 서버가 꺼져 있습니다.\n\nstart-all.ps1 을 실행하거나\n포트 " + v.port + " 서버를 켜주세요.");
				return;
			}
			doLaunch();
		});
	}

	function closeGame() {
		var overlay = $("#game-overlay");
		var frame = $("#game-frame");
		if (frame) frame.src = "about:blank";
		if (overlay) overlay.classList.remove("active");
		if (document.fullscreenElement && document.exitFullscreen) {
			document.exitFullscreen().catch(function() {});
		}
	}

	function bindSidebar() {
		$all(".sidebar .menu-item[data-sidebar]").forEach(function(item) {
			item.addEventListener("click", function(e) {
				e.preventDefault();
				var id = item.getAttribute("data-sidebar");
				if (!id) return;
				$all(".sidebar .menu-item").forEach(function(m) { m.classList.remove("active"); });
				item.classList.add("active");
				$all(".sidebar-view").forEach(function(v) { v.classList.remove("active"); });
				var view = document.getElementById("view-" + id);
				if (view) view.classList.add("active");
				if (id === "settings") renderInstallManager();
			});
		});
	}

	function bindSettingsTabs() {
		$all(".settings-tab").forEach(function(tab) {
			tab.addEventListener("click", function() {
				var pane = tab.getAttribute("data-pane");
				$all(".settings-tab").forEach(function(t) { t.classList.remove("active"); });
				$all(".settings-pane").forEach(function(p) { p.classList.remove("active"); });
				tab.classList.add("active");
				var el = document.getElementById("pane-" + pane);
				if (el) el.classList.add("active");
				if (pane === "installations") renderInstallManager();
			});
		});
	}

	function bindSettings() {
		var username = $("#setting-username");
		var defaultVersion = $("#setting-default-version");
		var fullscreen = $("#setting-fullscreen");
		var gift = $("#setting-gift-banner");
		var motion = $("#setting-reduce-motion");
		if (username) username.value = state.settings.username;
		if (fullscreen) fullscreen.checked = !!state.settings.fullscreenLaunch;
		if (gift) gift.checked = !!state.settings.showGiftBanner;
		if (motion) motion.checked = !!state.settings.reduceMotion;
		if (defaultVersion) {
			defaultVersion.innerHTML = "";
			installedCatalog().forEach(function(v) {
				var opt = document.createElement("option");
				opt.value = v.id;
				opt.textContent = v.name + " " + v.version;
				defaultVersion.appendChild(opt);
			});
			defaultVersion.value = state.settings.defaultVersionId;
		}
		$("#settings-save") && $("#settings-save").addEventListener("click", function() {
			state.settings.username = username ? username.value.trim() || "Player" : "Player";
			state.settings.defaultVersionId = defaultVersion ? defaultVersion.value : state.settings.defaultVersionId;
			state.settings.fullscreenLaunch = fullscreen ? fullscreen.checked : true;
			state.settings.showGiftBanner = gift ? gift.checked : true;
			state.settings.reduceMotion = motion ? motion.checked : false;
			saveSettings();
			applyMotionPref();
			updateSelectedUI();
			applyGiftBanner();
			showToast("설정이 저장되었습니다");
		});
	}

	function applyGiftBanner() {
		var gift = $(".gift-alert-container");
		if (gift) gift.style.display = state.settings.showGiftBanner ? "flex" : "none";
	}

	function bindGameFrame() {
		var frame = $("#game-frame");
		var overlay = $("#game-overlay");
		if (!frame || !overlay) return;
		overlay.addEventListener("click", function() {
			try {
				frame.focus();
				if (frame.contentWindow) frame.contentWindow.focus();
			} catch (e) {}
		});
	}

	function bindPlayButtons() {
		var mainPlay = $("#main-play-button");
		if (mainPlay) {
			mainPlay.addEventListener("click", function(e) {
				e.preventDefault();
				launchSelected();
			});
		}
		$("#close-game") && $("#close-game").addEventListener("click", closeGame);
		$(".gift-banner .close-x") && $(".gift-banner .close-x").addEventListener("click", function() {
			state.settings.showGiftBanner = false;
			saveSettings();
			applyGiftBanner();
		});
		$("#mc-modal-backdrop") && $("#mc-modal-backdrop").addEventListener("click", function() {
			if (state.modalResolve) closeModal(false);
		});
	}

	function spawnParticles() {
		if (state.settings.reduceMotion) return;
		var layer = $("#particle-layer");
		if (!layer) return;
		layer.innerHTML = "";
		for (var i = 0; i < 14; i++) {
			var p = document.createElement("div");
			p.className = "particle";
			p.style.left = (Math.random() * 100) + "%";
			p.style.animationDuration = (12 + Math.random() * 18) + "s";
			p.style.animationDelay = (Math.random() * 10) + "s";
			p.style.width = p.style.height = (6 + Math.random() * 10) + "px";
			p.style.opacity = (0.15 + Math.random() * 0.25);
			layer.appendChild(p);
		}
	}

	function init() {
		if (!isInstalled(state.settings.defaultVersionId)) {
			state.settings.defaultVersionId = state.settings.installedVersions[0] || "wasm-1122";
		}
		state.selectedId = state.settings.defaultVersionId;
		document.body.classList.add("launcher-ready");
		applyMotionPref();
		spawnParticles();
		bindSidebar();
		bindSettingsTabs();
		bindSettings();
		bindGameFrame();
		bindPlayButtons();
		updateSelectedUI();
		renderAllLists();
		renderInstallManager();
		applyGiftBanner();
		checkServers();
		setInterval(checkServers, 15000);
	}

	document.addEventListener("DOMContentLoaded", init);
})();
