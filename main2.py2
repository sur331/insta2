from instagrapi import Client

# تسجيل الدخول
cl = Client()
cl.login("اسم_حسابك", "كلمة_المرور")

# رابط المنشور الذي تريد الإعجاب به
media_url = "https://www.instagram.com/p/XXXXXXXXX/"

# الحصول على معرف المنشور والإعجاب به
media_id = cl.media_id(media_url)
cl.media_like(media_id)

print("تم الإعجاب بالمنشور بنجاح!")
