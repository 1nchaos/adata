import {defaultTheme, defineUserConfig} from 'vuepress'
import sidebar from "./sidebar";
import navbar from "./navbar";
import {searchPlugin} from "@vuepress/plugin-search";
import {seoPlugin} from "vuepress-plugin-seo2";
import clipboardPlugin from "vuepress-plugin-clipboard";

export default defineUserConfig({
    lang: 'zh-CN',
    title: 'AData',
    description: '专注股票量化数据，为Ai(爱)发电，向阳而生。',
    head: [
        ["link", {rel: "icon", href: "/favicon.ico"}],
        [
            "meta",
            {
                name: "keywords",
                content:
                    "免费开源A股量化数据库； 专注A股，专注量化，向阳而生； 开放、纯净、持续、为Ai(爱)发电。为个人量化交易而生，保卫3000点......【股票数据，股票行情数据，股票量化数据，k线行情数据，股票概念数据】"
            }
        ],
        [
            "meta",
            {
                name: "description",
                content:
                    "免费开源A股量化数据库； 专注A股，专注量化，向阳而生； 开放、纯净、持续、为Ai(爱)发电。为个人量化交易而生，保卫3000点......【股票数据，股票行情数据，股票量化数据，k线行情数据，股票概念数据】"
            }
        ]
    ],
    theme: defaultTheme({
        logo: "logo.png",
        repo: "1nchaos/adata",
        sidebar,
        navbar,
        editLink: false,
        contributors: false,
        lastUpdated: false
    }),
    plugins: [
        searchPlugin({
            locales: {
                '/': {
                    placeholder: '搜索',
                }
            },
        }),
        clipboardPlugin({
            align: "top",
            staticIcon: true
        }),
        seoPlugin({
            hostname: "https://github.com/1nchaos/adata",
            author: "1nchaos"
        })
    ]
})