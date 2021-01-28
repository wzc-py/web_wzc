import Vue from 'vue'
import Router from 'vue-router'
import Banner from "../components/Banner";
import Login from "../components/Login";
import Home from "../components/Home";
import Register from "../components/Register";
import Course from "../components/Course";
import Detail from "../components/Detail";
import Cart from "../components/Cart";

Vue.use(Router)

export default new Router({
    routes: [
        {path: "/login", component: Login},
        {path: "/register", component:Register},
        {path: "/course", component:Course},
        {path: "/detail/:id", component:Detail},
        {path: "/cart", component:Cart},
        {path: "/", component:Home},
        {path: "/*", component:Home},
    ]
})
