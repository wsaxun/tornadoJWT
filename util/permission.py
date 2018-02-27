# -*- coding: utf-8 -*-

from tornado.gen import coroutine, Return


class Permission(object):
    """ 验证权限
    """

    @coroutine
    def permission(self):
        if not hasattr(self, 'token_data'):
            raise Return(0)
        uri = self.request.path
        user = self.token_data['user']
        try:
            result = self.sessions.execute(
                "SELECT t_user.f_user AS t_user_f_user, t_user_group.f_user_group "
                "AS t_user_group_f_user_group, t_menu.f_uri AS t_menu_f_uri  "
                "FROM t_user INNER JOIN t_user_relation_group ON"
                " t_user.f_id = t_user_relation_group.f_user_id INNER JOIN"
                " t_user_group ON t_user_group.f_id = t_user_relation_group.f_user_group_id "
                "INNER JOIN t_permission ON "
                "t_user_group.f_id = t_permission.f_user_group_id INNER JOIN "
                "t_menu ON t_menu.f_id = t_permission.f_menu_id  WHERE "
                "t_menu.f_uri = '%s' AND t_user.f_user = '%s'" %(uri, user))
        except Exception:
            raise Return(0)
        result = result.rowcount
        raise Return(result)
