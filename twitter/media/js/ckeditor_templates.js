/*
Copyright (c) 2003-2009, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.addTemplates( 'twitter',
{
	// The name of sub folder which hold the shortcut preview images of the
	// templates.
	imagesPath : '/media/img/templates/',

	// The templates definitions.
	templates :
		[
			{
				title: 'Twitter Default',
				image: 'twitter_default.png',
				description: 'Tweets will look the same as the Twitter Homepage',
				html:
					'<style type="text/css">\n' +

					'div.widget_tweet:hover {\n' +
					'	background-color: #F7F7F7;\n' +
					'}\n' +

					'div.widget_tweet_body a:hover { \n' +
					'	text-decoration: underline !important; \n' +
					'}\n' +

					'div.widget_tweet {\n' +
					'	border-bottom: 1px solid #EEEEEE;\n' +
					'	padding: 10px 0 8px;\n' +
					'	position: relative;\n' +
					'	font-family: \'Lucida Grande\', sans-serif;\n' +
					'	font-size: 14px;\n' +
					'	line-height: 16px;\n' +
					'	background-color: white;\n' +
					'}\n' +

					'div.widget_tweet_img {\n' +
					'	height: 50px;\n' +
					'	width: 50px;\n' +
					'	float: left;\n' +
					'}\n' +

					'div.widget_tweet_img img { \n' +
					'	max-width: 48px; \n' +
					'	max-height: 48px; \n' +
					'	border: none;\n' +
					'}\n' +

					'div.widget_tweet_body a { \n' +
					'	color: #2276BB !important; \n' +
					'	text-decoration: none !important;\n' +
					'}\n' +

					'div.widget_tweet_body {\n' +
					'	margin-left: 56px;\n' +
					'	min-height: 48px;\n' +
					'}\n' +

					'a.widget_screenname { \n' +
					'	font-weight: bold;\n' +
					'}\n' +

					'div.widget_tweet_body span.widget_tweet_meta,\n' +
					'div.widget_tweet_body span.widget_tweet_meta a {\n' +
					'	color: #999999;\n' +
					'	font-size: 11px;\n' +
					'}\n' +

					'</style>\n' +

					'<div class="widget_tweet">\n' +
					'	<div class="widget_tweet_img">\n' +
					'		<a href="%SOURCE_URL%">%IMAGE%</a>\n' +
					'	</div>\n' +
					'	<div class="widget_tweet_body">\n' +
					'		<a href="%LINK%" class="widget_screenname">%SOURCE%</a>\n' +
					'		%TEXT%<br />\n' +
					'		<span class="widget_tweet_meta"><a href="%LINK%">%AGODAY%</a> from %TWITTER_SOURCE%</span> \n' +
					'	</div>\n' +
					'</div>'
			},
			{
				title: 'Twitter Widget',
				image: 'twitter_widget.png',
				description: 'Same style as the Twitter Widget',
				html:
					'<style type="text/css">\n' +

					'div.widget_tweet a:hover { \n' +
					'	text-decoration: underline !important;\n' +
					'}\n' +

					'div.widget_tweet a { \n' +
					'	color: #4AED05 !important;\n' +
					'	text-decoration: none !important;\n' +
					'}\n' +

					'div.widget_tweet {\n' +
					'	font-family: "lucida grande",lucida,tahoma,helvetica,arial,sans-serif !important;\n' +
					'	font-size: 12px;\n' +
					'	background-color: black;\n' +
					'	color: white;\n' +
					'	border-bottom: 1px dotted #DDDDDD;\n' +
					'	padding: 6px 8px;\n' +
					'}\n' +

					'div.widget_tweet span.widget_tweet_meta,\n' +
					'div.widget_tweet span.widget_tweet_meta a {\n' +
					'	color: white !important;\n' +
					'	font-size: 9px !important;\n' +
					'}\n' +

					'</style>\n' +

					'<div class="widget_tweet">\n' +
					'	%TEXT%<br />\n' +
					'	<span class="widget_tweet_meta">\n' +
					'		<a href="%LINK%">%AGODAY%</a> \n' +
					'		by <a href="%SOURCE%">%SOURCE%</a>\n' +
					'	</span> \n' +
					'</div>\n'
			},
			{
				title: 'News Style',
				image: 'news.png',
				description: 'Tweets in a News Style',
				html:
					'<style type="text/css">\n' +

					'div.widget_tweet a { \n' +
					'	color: #2276BB !important; \n' +
					'	text-decoration: none !important;\n' +
					'}\n' +

					'div.widget_tweet a:hover { \n' +
					'	text-decoration: underline !important; \n' +
					'}\n' +

					'div.widget_tweet {\n' +
					'	font-family: \'Lucida Grande\', sans-serif;\n' +
					'	font-size: 14px;\n' +
					'	line-height: 16px;\n' +
					'	background-color: white;\n' +
					'	border-bottom: 1px solid #EEEEEE;\n' +
					'	padding: 10px 0 8px;\n' +
					'	position: relative;\n' +
					'}\n' +

					'div.widget_tweet span.widget_tweet_meta,\n' +
					'div.widget_tweet span.widget_tweet_meta a {\n' +
					'	color: #999999 !important;\n' +
					'	font-size: 11px !important;\n' +
					'}\n' +

					'</style>\n' +

					'<div class="widget_tweet">\n' +
					'	<span class="widget_tweet_meta">\n' +
					'		<a href="%LINK%">%AGODAY%</a> \n' +
					'		by <a href="%SOURCE%">%SOURCE%</a>\n' +
					'	</span><br />\n' +
					'	%TEXT%\n' +
					'</div>\n'
			}
		]
});
