import os
import datetime
import webapp2 as webapp

from google.appengine.api import memcache
from google.appengine.api import users

import model.forum
import ctrl.blog
import handlers
import handlers.admin


class ForumAdminPage(handlers.admin.AdminPage):
  pass


class DashboardPage(ForumAdminPage):
  def get(self):
    self.render("admin/forum/dashboard.html", {})


class ForumListPage(ForumAdminPage):
  def get(self):
    forums = []
    for forum in model.forum.Forum.all():
      forums.append(forum)

    self.render("admin/forum/forum_list.html", {"forums": forums})


class ForumEditPage(ForumAdminPage):
  def get(self, id=None):
    data = {}
    if id:
      data["forum"] = model.forum.Forum.get_by_id(int(id))
      forum_moderators_string = []
      for user in data["forum"].moderators:
        forum_moderators_string.append(user.email())
      data["forum_moderators_string"] = ", ".join(forum_moderators_string)
    else:
      data["forum"] = None

    self.render("admin/forum/forum_edit.html", data)

  def post(self, id=None):
    if id:
      forum = model.forum.Forum.get_by_id(int(id))
    else:
      forum = model.forum.Forum()

    old_slug = forum.slug
    forum.name = self.request.POST.get("forum-name")
    forum.slug = self.request.POST.get("forum-slug")
    forum.description = self.request.POST.get("forum-desc")
    if self.request.POST.get("forum-moderators"):
      forum.moderators = []
      for email in self.request.POST.get("forum-moderators").split(","):
        try:
          user = users.User(email.strip())
          forum.moderators.append(user)
        except users.UserNotFoundError:
          pass
    forum.put()
    memcache.delete("forums")
    memcache.delete("forums:%s" % (old_slug))
    memcache.delete("forums:%s" % (forum.slug))

    self.redirect("/admin/forum/forums/edit/"+str(forum.key().id_or_name()))


app = webapp.WSGIApplication([("/admin/forum/?", DashboardPage),
                              ("/admin/forum/forums/?", ForumListPage),
                              ("/admin/forum/forums/edit", ForumEditPage),
                              ("/admin/forum/forums/edit/(.*)", ForumEditPage)],
                             debug=os.environ['SERVER_SOFTWARE'].startswith('Development'))
