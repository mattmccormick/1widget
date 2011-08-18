<style type="text/css">
div.widget_tweet:hover {ldelim}
	background-color: #F7F7F7;
{rdelim}
div.widget_tweet_body a:hover {ldelim} 
	text-decoration: underline !important; 
{rdelim}
div.widget_tweet {ldelim}
	border-bottom: 1px solid #EEEEEE;
	padding: 10px 0 8px;
	position: relative;
	font-family: 'Lucida Grande', sans-serif;
	font-size: 14px;
	line-height: 16px;
	background-color: white;
{rdelim}
div.widget_tweet_img {ldelim}
	height: 50px;
	width: 50px;
	float: left;
{rdelim}
div.widget_tweet_img img {ldelim} 
	max-width: 48px; 
	max-height: 48px; 
	border: none;
{rdelim}
div.widget_tweet_body a {ldelim} 
	color: #2276BB !important; 
	text-decoration: none !important;
{rdelim}
div.widget_tweet_body {ldelim}
	margin-left: 56px;
	min-height: 48px;
{rdelim}
a.widget_screenname {ldelim} 
	font-weight: bold;
{rdelim}
div.widget_tweet_body span.widget_tweet_meta,
div.widget_tweet_body span.widget_tweet_meta a {ldelim}
	color: #999999;
	font-size: 20px;
{rdelim}
</style><div id="widget">{section name=i loop=$feeds}
<div class="widget_tweet">
	<div class="widget_tweet_img">
		<a href="%SOURCE_URL%">%IMAGE%</a></div>
	<div class="widget_tweet_body">
		<a class="widget_screenname" href="%LINK%">%SOURCE%</a> %TEXT%<br />
		<span class="widget_tweet_meta"><a href="%LINK%">%AGODAY%</a> from %TWITTER_SOURCE%</span></div>
</div>{/section}</div>