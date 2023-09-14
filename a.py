from requests_html import HTMLSession

session = HTMLSession()

url = 'https://laz-g-cdn.alicdn.com/??lzdpage/flash-sale-daraz/5.2.37/pc/index.js,lzdmod/act-loading/5.1.6/index.js,lzdmod/act-loading/5.1.6/detection.js,mui/jquery/5.0.2/jquery.js,lzdpage/flash-sale-daraz/5.2.37/i18n.js'

r = session.get(url)

r.html.render()

print(r.text)
# with open('a.html','w', encoding = 'utf-8') as f:
# 	f.write(r.text)
