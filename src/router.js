import Vue from "vue";
import VueRouter from "vue-router";
import StoreHome from "@/pages/store/Home";
import LibraryHome from "@/pages/library/Home";
import Login from "./pages/Login";

import HomeTemplate from "@/pages/templates/HomeTemplate";
import WithdrawGame from "@/pages/library/WithdrawGame";
import AddGame from "@/pages/library/AddGame";
import LibraryDashboard from "@/pages/library/Dashboard";

import authorizationService from "@/services/authorization.service";
import PageNotFound from "@/pages/PageNotFound";

Vue.use(VueRouter);

//Guardians
function guardAuthenticated(to, from, next) {
  if (authorizationService.isAuthenticated()) {
    next();
  } else {
    next({ name: "Login" });
  }
}

const routes = [
  {
    path: "",
    component: HomeTemplate,
    children: [
      {
        path: "/",
        name: "Home",
        component: LibraryHome,
        props: { title: "Library", pretitle: "leiriacon 2022" }
      },
      {
        path: "/library/",
        name: "LibraryHome",
        component: LibraryHome,
        props: { title: "Library", pretitle: "leiriacon 2022" }
      },
      {
        path: "/library/dashboard",
        name: "LibraryDashboard",
        beforeEnter: guardAuthenticated,
        component: LibraryDashboard
      },
      {
        path: "/store/",
        name: "StoreHome",
        component: StoreHome
      }
    ]
  },

  {
    path: "/library/new",
    name: "AddLibraryGame",
    beforeEnter: guardAuthenticated,
    component: AddGame
  },
  {
    path: "/library/:id/withdraw",
    name: "WithdrawGame",
    props: { title: "Withdraw game", pretitle: "Library" },
    beforeEnter: guardAuthenticated,
    component: WithdrawGame
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    beforeEnter: (to, from, next) => {
      if (authorizationService.isAuthenticated()) {
        next({ name: "NotFound" });
      } else {
        next();
      }
    }
  },
  {
    name: "NotFound",
    path: "*",
    component: PageNotFound
  }
];

const router = new VueRouter({
  mode: "history",
  base: "/",
  routes
});

export default router;