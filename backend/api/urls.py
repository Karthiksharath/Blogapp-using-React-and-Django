from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views


urlpatterns = [

    path('user/token/', api_views.TokenObtainView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', api_views.RegisterView.as_view(), name='auth_register'),
    path('user/profile/<user_id>/', api_views.ProfileView.as_view(), name='user_profile'),


    path('post/category/list/', api_views.CategoryListAPIView.as_view()),
    path('post/category/posts/<category_slug>/', api_views.PostCategoryListAPIView.as_view()),
    path('post/lists/', api_views.PostListApiView.as_view()),
    path('post/detail/<slug>/', api_views.PostDetailApiView.as_view()),
    path('post/like-post/', api_views.PostLikeApiView.as_view()),
    path('post/comment-post/', api_views.PostCommentAPIView.as_view()),
    path('post/bookmark-post/', api_views.BookMarkPostApiView.as_view()),

    path('author/dashboard/stats/<user_id>/', api_views.DashboardStats.as_view()),
    path('author/dashboard/post-lists/<user_id>/', api_views.DashboardPostLists.as_view()),
    path('author/dashboard/comment-lists/<user_id>/', api_views.DashboardCommentLists.as_view()),
    path('author/dashboard/notifiaction-list/<user_id>/', api_views.DashboardNotificationLists.as_view()),
    path('author/dashboard/notification-mark-seen/', api_views.DashboardMarkNotificationSeenAPIView.as_view()),
    path('author/dashboard/reply-comment/', api_views.DashboardPostCommentAPIView.as_view()),
    path('author/dashboard/reply-comment/', api_views.DashboardPostCommentAPIView.as_view()),
    path('author/dashboard/post-create/', api_views.DashboardPostCreateAPIView.as_view()),
    path('author/dashboard/post-detail/<user_id>/<post_id>/', api_views.DashboardPostEditAPIView.as_view()),
    
]