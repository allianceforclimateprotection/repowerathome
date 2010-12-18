({
    appDir: "../static",
    baseUrl: "js",
    dir: "../static_build",
    optimizeCss: "standard",
    modules: [
        {
            name: "pages/base",
            include: ["libs/webfont", "libs/jquery.ui", "libs/jquery.form", "libs/jquery.validation", "mods/feedback", "mods/messages", "mods/facebook", "pages/base"]
        },
        {
            name: "pages/rah.home_logged_out",
            exclude: ["pages/base"],
            include: ["libs/jquery.cookie", "mods/pledge"]
        },
        {
            name: "pages/rah.home_logged_in",
            exclude: ["pages/base"],
            include: ["mods/pledge", "mods/invite", "mods/commitments"]
        },
        {
            name: "pages/rah.login",
            exclude: ["pages/base"],
        },
        {
            name: "pages/rah.register",
            exclude: ["pages/base"],
        },
        {
            name: "pages/rah.profile.edit",
            exclude: ["pages/base"],
        }
    ]
})
