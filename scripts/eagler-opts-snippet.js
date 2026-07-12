// Shared eaglercraftXOpts for cleaned local client (Korean default, minimal branding UI)
function buildEaglercraftXOpts(containerOrRelayId) {
	var relayId = typeof containerOrRelayId === "number"
		? containerOrRelayId
		: Math.floor(Math.random() * 3);
	var opts = {
		demoMode: false,
		worldsDB: "worlds",
		lang: "ko_kr",
		localesURI: "lang/",
		showBootMenuOnLaunch: false,
		allowBootMenu: false,
		bootMenuBlocksUnsignedClients: false,
		enableSignatureBadge: false,
		enableDownloadOfflineButton: false,
		allowUpdateSvc: false,
		allowUpdateDL: false,
		enableMinceraft: false,
		forceProfanityFilter: false,
		html5CursorSupport: true,
		openDebugConsoleOnLaunch: false,
		logInvalidCerts: false,
		crashOnUncaughtExceptions: true,
		checkRelaysForUpdates: true,
		allowServerRedirects: true,
		relays: [
			{ addr: "wss://relay.deev.is/", comment: "relay #1", primary: relayId === 0 },
			{ addr: "wss://relay.lax1dude.net/", comment: "relay #2", primary: relayId === 1 },
			{ addr: "wss://relay.shhnowisnottheti.me/", comment: "relay #3", primary: relayId === 2 }
		]
	};
	if (typeof containerOrRelayId === "string") {
		opts.container = containerOrRelayId;
		opts.assetsURI = "assets.epk";
	}
	return opts;
}
