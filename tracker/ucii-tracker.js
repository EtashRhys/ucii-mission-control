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

                throw new Error(
                    "UCIITracker requires an endpoint"
                );

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



        generateId() {


            if (
                window.crypto &&
                typeof window.crypto.randomUUID === "function"
            ) {

                return window.crypto.randomUUID();

            }


            return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
                /[xy]/g,
                function (c) {

                    const r = Math.random() * 16 | 0;

                    const v = c === "x"
                        ? r
                        : (r & 0x3 | 0x8);


                    return v.toString(16);

                }
            );

        },



        getOrCreateId(key, persistent) {


            const storage = persistent
                ? window.localStorage
                : window.sessionStorage;



            let id = storage.getItem(key);



            if (!id) {

                id = this.generateId();

                storage.setItem(
                    key,
                    id
                );

            }



            return id;

        },



        getEnvironmentMetadata() {


            return {

                user_agent:
                    navigator.userAgent,


                platform:
                    navigator.platform || null,


                language:
                    navigator.language || null,


                timezone:
                    Intl.DateTimeFormat().resolvedOptions().timeZone || null,


                screen:
                {

                    width:
                        window.screen.width,


                    height:
                        window.screen.height

                },


                viewport:
                {

                    width:
                        window.innerWidth,


                    height:
                        window.innerHeight

                }

            };


        },



        sendEvent(eventType, extra) {


            const metadata = Object.assign(

                {},

                this.getEnvironmentMetadata(),

                extra || {}

            );



            const payload = {


                event_type:
                    eventType,


                visitor_id:
                    this.visitorId,


                session_id:
                    this.sessionId,


                url:
                    window.location.pathname,


                referrer:
                    document.referrer || null,


                metadata:
                    metadata

            };



            fetch(
                this.config.endpoint,
                {

                    method:
                        "POST",


                    headers:
                    {

                        "Content-Type":
                            "application/json"

                    },


                    body:
                        JSON.stringify(payload),


                    keepalive:
                        true

                }

            ).catch(function () {

                // telemetry failure is intentionally ignored

            });


        },



        trackPageView() {


            this.sendEvent(
                "page_view"
            );


        },



        startHeartbeat() {


            const self = this;



            window.setInterval(function () {


                self.sendEvent(
                    "heartbeat"
                );


            }, 60000);


        },



        registerPageLeave() {


            const self = this;



            window.addEventListener(
                "beforeunload",
                function () {


                    const payload =
                        JSON.stringify({

                            event_type:
                                "page_leave",


                            visitor_id:
                                self.visitorId,


                            session_id:
                                self.sessionId,


                            url:
                                window.location.pathname,


                            referrer:
                                document.referrer || null,


                            metadata:
                                self.getEnvironmentMetadata()

                        });



                    if (navigator.sendBeacon) {


                        navigator.sendBeacon(

                            self.config.endpoint,

                            payload

                        );

                    }


                }

            );


        }


    };



    window.UCIITracker = UCIITracker;


})(window);
