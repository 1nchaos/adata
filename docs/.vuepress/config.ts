// @ts-ignore
import clipboardPlugin from "vuepress-plugin-clipboard";
import sidebar from "./sidebar";
import navbar from "./navbar";

const { defineUserConfig } = require("vuepress");
const { defaultTheme } = require("vuepress");
const { searchPlugin } = require("@vuepress/plugin-search");
// @ts-ignore
import { seoPlugin } from "vuepress-plugin-seo2";
// @ts-ignore
import { sitemapPlugin } from "vuepress-plugin-sitemap2";
// @ts-ignore
import { searchConsolePlugin } from "vuepress-plugin-china-search-console";

export default defineUserConfig({
  title: "adata",
  description: "向阳而生",
  head: [
    ["link", { rel: "icon", href: "/favicon.ico" }],
    [
      "meta",
      {
        name: "keywords",
        content:
          "编"
      }
    ],
    [
      "meta",
      {
        name: "description",
        content:
          "帮"
      }
    ],
    [
      "script",
      {
        async: true,
        src: "https://www.googletagmanager.com/gtag/js?id=G-1X4BRVH78Z"
      }
    ],
    [
      "script",
      {},
      `window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-1X4BRVH78Z');`
    ]
  ],
  theme: defaultTheme({
    logo: "logo.png",
    repo: "liyupi/code-xingqiu",
    sidebar,
    navbar,
    editLink: false,
    smoothScroll: true,
    contributors: false,
    lastUpdated: false
  }),
  plugins: [
    searchPlugin({
      // 配置项
    }),
    clipboardPlugin({
      align: "top",
      staticIcon: true
    }),
    seoPlugin({
      hostname: "",
      author: ""
    }),
    sitemapPlugin({
      hostname: ""
    }),
    searchConsolePlugin({
      // 改成自己的百度统计 id：https://tongji.baidu.com/
      baiduId: "d6dba90b6d34581f364377a36215fd26"
    })
  ]
});
