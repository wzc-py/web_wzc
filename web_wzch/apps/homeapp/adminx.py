import xadmin
from xadmin import views

from homeapp.models import Banner, Nav


# xadmin的基本配置
class BaseSetting(object):
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    site_title = "百知教育后台信息管理系统"  # 设置站点标题
    site_footer = "北京百知教育科技有限公司"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSetting)


# 将轮播图注册到后台站点
class BannerInfo(object):
    list_display = ["title", "orders", "is_show", "img"]


xadmin.site.register(Banner, BannerInfo)


# 导航栏注册到后台站点
class NavInfo(object):
    list_display = ["title", "orders", "is_show"]


xadmin.site.register(Nav, NavInfo)
