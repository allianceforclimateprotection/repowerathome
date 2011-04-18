({
    appDir: "../static",
    baseUrl: "js",
    dir: "../static_build",
    optimizeCss: "standard.keepLines",
    modules: [
        {
            name: "pages/base",
            include: ["libs/jquery.ui", "libs/jquery.form", "libs/jquery.validation", "mods/messages", "mods/facebook"] 
        },
        {
            name: "pages/rah.home",
            exclude: ["pages/base"],
            include: ["libs/jquery.cookie"]
        },
        {
            name: "pages/rah.login",
            exclude: ["pages/base"]
        },
        {
            name: "pages/rah.register",
            exclude: ["pages/base"]
        },
        {
            name: "pages/rah.profile.edit",
            exclude: ["pages/base"]
        },
        {
            name: "pages/blog.post_detail",
            exclude: ["pages/base"],
            include: ["libs/jquery.qtip", "mods/comments"]
        },
        {
            name: "pages/registration.password_change",
            exclude: ["pages/base"]
        },
        {
            name: "pages/registration.password_reset_confirm",
            exclude: ["pages/base"]
        },
        {
            name: "pages/group.create",
            exclude: ["pages/base"],
            include: ["libs/jquery.prepopulate"]
        },
        {
            name: "pages/group.detail",
            exclude: ["pages/base"],
            include: ["libs/jquery.tablesorter", "mods/invite"]
        },
        {
            name: "pages/group.edit",
            exclude: ["pages/base"]
        },
        {
            name: "pages/events.show",
            exclude: ["pages/base"],
            include: ["libs/markerclusterer", "mods/search"]
        },
        {
            name: "pages/events.detail",
            exclude: ["pages/base"],
            include: ["libs/jquery.qtip", "libs/jquery.jeditable", "mods/comments", "mods/events", "mods/commitments"]
        },
        {
            name: "pages/events.create",
            exclude: ["pages/base"],
            include: ["libs/jquery.qtip", "libs/jquery.jeditable"]
        },
        {
            name: "pages/commitments.show",
            exclude: ["pages/base"],
            include: ["mods/commitments"]
        },
        {
            name: "pages/commitments.card",
            exclude: ["pages/base"],
            include: ["mods/commitments"]
        },
        {
            name: "pages/group.list",
            exclude: ["pages/base"],
            include: ["mods/search"]
        },
        {
            name: "pages/action.detail",
            exclude: ["pages/base"],
            include: ["mods/comments", "libs/jquery.qtip"]
        }
    ]
})
