(function (window) {
    "use strict";

    const UCIITracker = {
        config: {
            endpoint: null
        },

        visitorId: null,
        sessionId: null,

        init(options) {
            if (!options || !options.endpoint) {
                throw new Error("UCIITracker requires an endpoint");
            }

            this.config.endpoint = options.endpoint;

            this.initializeIdentity();
            this.trackPageView();
            this.startHeartbeat();
            this.registerPageLeave();
        },

        initializeIdentity() {
            this.visitorId = this.getOrCreateId(
                "ucii_visitor_id",
                true
            );

            this.sessionId = this.getOrCreateId(
                "ucii_session_id",
                false
            );
        },

        getOrCreateId(key, persistent) {
            const storage = persistent
                ? window.localStorage
                : window.sessionStorage;

            let id = storage.getItem(key);

            if (!id) {
                id = crypto.randomUUID();
                storage.setItem(key, id);
            }

            return id;
        },

        sendEvent(eventType, extra) {
            const payload = {
                event_type: eventType,
                visitor_id: this.visitorId,
                session_id: this.sessionId,
                url: window.location.pathname,
                referrer: document.referrer || null,
                metadata: extra || {}
            };

            fetch(this.config.endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload),
                keepalive: true
            }).catch(function () {
                // Silent failure by design.
                // Telemetry should never break the host application.
            });
        },

        trackPageView() {
            this.sendEvent("page_view");
        },

        startHeartbeat() {
            const self = this;

            window.setInterval(function () {
                self.sendEvent("heartbeat");
            }, 60000);
        },

        registerPageLeave() {
            const self = this;

            window.addEventListener("beforeunload", function () {
                const payload = JSON.stringify({
                    event_type: "page_leave",
                    visitor_id: self.visitorId,
                    session_id: self.sessionId,
                    url: window.location.pathname,
                    referrer: document.referrer || null,
                    metadata: {}
                });

                if (navigator.sendBeacon) {
                    navigator.sendBeacon(
                        self.config.endpoint,
                        payload
                    );
                }
            });
        }
    };

    window.UCIITracker = UCIITracker;

})(window);
