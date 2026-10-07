```javascript
/* =========================================================
   AZIZI & CO
   ADVANCED INTERACTION ENGINE

   GSAP
   ScrollTrigger
   Barba.js

   IMPORTANT:
   Native browser scrolling is intentionally used.
   Lenis has been removed because the cinematic homepage
   already uses ScrollTrigger + scrub.
========================================================= */


/* =========================================================
   GLOBAL STATE
========================================================= */

let aziziInitialized = false;


/* =========================================================
   GSAP INITIALIZATION
========================================================= */

const initGSAP = () => {

    if (
        typeof gsap === "undefined" ||
        typeof ScrollTrigger === "undefined"
    ) {
        console.warn(
            "AZIZI & CO: GSAP or ScrollTrigger is unavailable."
        );

        return false;
    }


    gsap.registerPlugin(ScrollTrigger);


    /*
     * Prevent ScrollTrigger from fighting native scrolling.
     *
     * GSAP handles the animation.
     * The browser handles the actual wheel movement.
     */

    ScrollTrigger.config({
        ignoreMobileResize: true
    });


    return true;
};


/* =========================================================
   MAGNETIC BUTTONS
========================================================= */

const initMicroInteractions = () => {

    const buttons =
        document.querySelectorAll(".magnetic-btn");


    buttons.forEach((button) => {

        /*
         * Prevent duplicate event listeners when Barba
         * loads a new page.
         */

        if (
            button.dataset.magneticInitialized === "true"
        ) {
            return;
        }


        button.dataset.magneticInitialized = "true";


        button.addEventListener(
            "mousemove",
            (event) => {

                const rect =
                    button.getBoundingClientRect();


                const x =
                    event.clientX -
                    rect.left -
                    rect.width / 2;


                const y =
                    event.clientY -
                    rect.top -
                    rect.height / 2;


                gsap.to(
                    button,
                    {
                        x: x * 0.14,
                        y: y * 0.14,

                        duration: 0.35,

                        ease: "power3.out",

                        overwrite: true
                    }
                );

            }
        );


        button.addEventListener(
            "mouseleave",
            () => {

                gsap.to(
                    button,
                    {
                        x: 0,
                        y: 0,

                        duration: 0.7,

                        ease:
                            "elastic.out(1, .35)",

                        overwrite: true
                    }
                );

            }
        );

    });

};


/* =========================================================
   HEADER SCROLL EFFECT
========================================================= */

const initHeader = () => {

    const header =
        document.querySelector(".site-header");


    if (!header) {
        return;
    }


    const updateHeader = () => {

        const scrolled =
            window.scrollY > 35;


        if (scrolled) {

            header.style.background =
                "rgba(5,5,5,.92)";

            header.style.borderColor =
                "rgba(255,255,255,.11)";

        } else {

            header.style.background =
                "linear-gradient(to bottom, rgba(5,5,5,.96), rgba(5,5,5,.78))";

            header.style.borderColor =
                "rgba(255,255,255,.075)";
        }

    };


    updateHeader();


    window.addEventListener(
        "scroll",
        updateHeader,
        {
            passive: true
        }
    );

};


/* =========================================================
   PAGE VISIBILITY
========================================================= */

const initPageReveal = () => {

    const container =
        document.querySelector(
            '[data-barba="container"]'
        );


    if (!container) {
        return;
    }


    gsap.set(
        container,
        {
            opacity: 1,
            filter: "blur(0px)",
            scale: 1
        }
    );

};


/* =========================================================
   BARBA.JS
========================================================= */

const initBarba = () => {

    if (typeof barba === "undefined") {

        console.warn(
            "AZIZI & CO: Barba.js is unavailable."
        );

        return;
    }


    if (
        window.__AZIZI_BARBA_INITIALIZED__
    ) {
        return;
    }


    window.__AZIZI_BARBA_INITIALIZED__ =
        true;


    barba.init({

        /*
         * Do NOT synchronize the old and new
         * pages during the transition.
         *
         * This prevents weird scroll behavior.
         */

        sync: false,


        transitions: [

            {

                name:
                    "azizi-cinematic-transition",


                async leave(data) {

                    await gsap.to(
                        data.current.container,
                        {
                            opacity: 0,

                            scale: 0.985,

                            filter:
                                "blur(8px)",

                            duration: 0.35,

                            ease:
                                "power2.inOut"
                        }
                    );

                },


                async beforeEnter(data) {

                    /*
                     * Destroy triggers belonging to
                     * the old page.
                     */

                    if (
                        typeof ScrollTrigger !==
                        "undefined"
                    ) {

                        ScrollTrigger
                            .getAll()
                            .forEach(
                                trigger =>
                                    trigger.kill()
                            );

                    }


                    /*
                     * Native browser scroll.
                     */

                    window.scrollTo(
                        0,
                        0
                    );

                },


                async enter(data) {

                    gsap.fromTo(
                        data.next.container,

                        {
                            opacity: 0,

                            scale: 1.015,

                            filter:
                                "blur(8px)"
                        },

                        {
                            opacity: 1,

                            scale: 1,

                            filter:
                                "blur(0px)",

                            duration: 0.55,

                            ease:
                                "power3.out"
                        }
                    );

                },


                async afterEnter() {

                    /*
                     * Reinitialize page-specific
                     * interactions.
                     */

                    initMicroInteractions();

                    initHeader();


                    /*
                     * Give the browser time to
                     * finish layout before refreshing
                     * ScrollTrigger.
                     */

                    requestAnimationFrame(
                        () => {

                            requestAnimationFrame(
                                () => {

                                    if (
                                        typeof ScrollTrigger !==
                                        "undefined"
                                    ) {

                                        ScrollTrigger
                                            .refresh();
                                    }

                                }
                            );

                        }
                    );

                }

            }

        ]

    });

};


/* =========================================================
   RESIZE HANDLING
========================================================= */

const initResizeHandling = () => {

    let resizeTimer;


    window.addEventListener(
        "resize",
        () => {

            clearTimeout(resizeTimer);


            resizeTimer =
                setTimeout(
                    () => {

                        if (
                            typeof ScrollTrigger !==
                            "undefined"
                        ) {

                            ScrollTrigger.refresh();

                        }

                    },
                    250
                );

        }
    );

};


/* =========================================================
   BOOTSTRAP
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        if (aziziInitialized) {
            return;
        }


        aziziInitialized = true;


        initGSAP();

        initPageReveal();

        initMicroInteractions();

        initHeader();

        initResizeHandling();

        initBarba();

    }
);
```
