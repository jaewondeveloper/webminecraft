"use strict";

(function() {
	var PACK_ZIP = "resourcepacks/Astra.zip";
	var PACK_ID = "astra_1192_locked";
	var PACK_LABEL = "Astra";
	var STORAGE_NS = "_eaglercraftX_astra";
	var PACK_DB = "resourcePacks_astra";

	function log(msg) {
		if (typeof window.__eaglerSetLoadingStatus === "function") {
			window.__eaglerSetLoadingStatus(msg);
		}
	}

	function openDb(name) {
		return new Promise(function(resolve, reject) {
			var req = indexedDB.open(name, 2);
			req.onupgradeneeded = function(ev) {
				var db = ev.target.result;
				if (!db.objectStoreNames.contains("files")) db.createObjectStore("files");
				if (!db.objectStoreNames.contains("meta")) db.createObjectStore("meta");
			};
			req.onsuccess = function() { resolve(req.result); };
			req.onerror = function() { reject(req.error); };
		});
	}

	function idbPut(db, store, key, val) {
		return new Promise(function(resolve, reject) {
			var tx = db.transaction(store, "readwrite");
			tx.objectStore(store).put(val, key);
			tx.oncomplete = function() { resolve(); };
			tx.onerror = function() { reject(tx.error); };
		});
	}

	function idbGet(db, store, key) {
		return new Promise(function(resolve, reject) {
			var tx = db.transaction(store, "readonly");
			var req = tx.objectStore(store).get(key);
			req.onsuccess = function() { resolve(req.result); };
			req.onerror = function() { reject(req.error); };
		});
	}

	function loadScript(url) {
		return new Promise(function(resolve, reject) {
			if (window.JSZip) { resolve(); return; }
			var s = document.createElement("script");
			s.src = url;
			s.onload = resolve;
			s.onerror = reject;
			document.head.appendChild(s);
		});
	}

	async function installPackFromZip() {
		var db = await openDb(PACK_DB);
		var done = await idbGet(db, "meta", "astra_installed_v2");
		if (done) return;

		log("Astra 리소스팩 설치 중...");
		await loadScript("https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js");
		var res = await fetch(PACK_ZIP);
		if (!res.ok) throw new Error("Astra.zip not found");
		var buf = await res.arrayBuffer();
		var zip = await window.JSZip.loadAsync(buf);
		var files = Object.keys(zip.files);
		var count = 0;
		for (var i = 0; i < files.length; i++) {
			var entry = zip.files[files[i]];
			if (entry.dir) continue;
			var data = await entry.async("uint8array");
			await idbPut(db, "files", PACK_ID + "/" + files[i], data);
			count++;
			if (count % 200 === 0) log("Astra 리소스팩 설치 중... " + count + "/" + files.length);
		}
		var manifest = {
			version: 4,
			packs: {}
		};
		manifest.packs[PACK_ID] = {
			name: PACK_LABEL,
			folder: PACK_ID,
			type: "folder",
			locked: true,
			fileCount: count,
			timestamp: Date.now()
		};
		await idbPut(db, "meta", "manifest.json", JSON.stringify(manifest));
		await idbPut(db, "meta", "astra_installed_v2", true);
		log("Astra 리소스팩 설치 완료");
	}

	function enforceOptions() {
		try {
			for (var i = 0; i < localStorage.length; i++) {
				var key = localStorage.key(i);
				if (!key || key.indexOf(STORAGE_NS) === -1) continue;
				var val = localStorage.getItem(key);
				if (!val || val.indexOf("resourcePacks:") === -1) continue;
				if (val.indexOf(PACK_ID) !== -1) continue;
				if (val.indexOf("resourcePacks:[]") !== -1) {
					localStorage.setItem(key, val.replace("resourcePacks:[]", 'resourcePacks:["' + PACK_ID + '"]'));
				} else if (val.indexOf("resourcePacks:[") !== -1) {
					localStorage.setItem(key, val.replace("resourcePacks:[", 'resourcePacks:["' + PACK_ID + '",'));
				}
			}
		} catch (e) {}
	}

	function waitForCanvas(cb) {
		var n = 0;
		var t = setInterval(function() {
			if (document.querySelector("._eaglercraftX_canvas_element")) {
				clearInterval(t);
				cb();
				return;
			}
			if (++n > 500) clearInterval(t);
		}, 200);
	}

	window.addEventListener("load", function() {
		waitForCanvas(function() {
			installPackFromZip().then(function() {
				enforceOptions();
				setInterval(enforceOptions, 4000);
			}).catch(function(e) {
				console.error(e);
				log("Astra 팩 설치 실패");
			});
		});
	});
})();
