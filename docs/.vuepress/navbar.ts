import { NavbarConfig } from "@vuepress/theme-default/lib/shared/nav";

export default [
    {text: '向阳花', link: '/向阳花.md'},
    {text: '数据源',
     collapsible: true,
          children: [
              {text:'同花顺',link:'https://www.10jqka.com.cn/'},
              {text:'百度股市通',link:'https://gushitong.baidu.com/stock/ab-300033'},
          ]
    },
] as NavbarConfig;