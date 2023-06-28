// @ts-ignore
import {SidebarConfig} from "@vuepress/theme-default/lib/shared/nav";

export default [
    {
        text: '星球介绍',
        link: '/',
    },
    {
        text: '星球资料',
        collapsible: true,
        children: ['/星球资料/学习资源', '/星球资料/学习路线', '/星球资料/专属交流群', '/星球资料/鱼皮的学习笔记', '/星球资料/鱼皮的打工日记'],
    },
    '/大家的真实评价',
    {
        text: '星球项目',
        collapsible: true,
        children: ['/星球项目/项目训练营', '/星球项目/用户中心项目', '/星球项目/伙伴匹配系统', '/星球项目/API开放平台', '/星球项目/聚合搜索平台',
            '/星球项目/Java 后端万用项目模板', '/星球项目/Web 终端项目', '/星球项目/编程导航奖励系统', '/星球项目/SQL 生成器项目',
            '/星球项目/工作记录分析工具'],
    },
    {
        text: '星球直播',
        collapsible: true,
        children: ['/星球直播/', '/星球直播/项目训练营', '/星球直播/往期直播', '/星球直播/嘉宾分享'],
    },
    '/星球故事',
    {
        text: '关于星主',
        collapsible: true,
        children: ['/关于星主/', '/关于星主/个人经历'],
    },
    '/星球年度总结',
    '/加入星球',
] as SidebarConfig;