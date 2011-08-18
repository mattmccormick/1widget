<div id="widget">{section name=i loop=$tweets}<style type="text/css">

div#widget {
	font-family: 'Lucida Grande', sans-serif;
	font-size: 14px;
	line-height: 16px;
	background-color: white;
}

div.widget_tweet_body a { 
	color: #2276BB; 
	text-decoration: none;
}

div#widget a:hover { 
	text-decoration: underline; 
}

div.widget_tweet {
	border-bottom: 1px solid #EEEEEE;
	padding: 10px 0 8px;
	position: relative;
}

div.widget_tweet:hover {
	background-color: #F7F7F7;
}

div.widget_tweet_img {
	margin: 0 10px 0 0;
	position: absolute;
}

div.widget_tweet img { 
	width: 48px; 
	height: 48px; 
	border: none;
}

div.widget_tweet_body {
	margin-left: 56px;
	min-height: 48px;
}

a.widget_screenname { 
	font-weight: bold;
}

div.widget_tweet_body span.widget_tweet_meta,
div.widget_tweet_body span.widget_tweet_meta a {
	color: #999999;
	font-size: 11px;
}

</style>
<div class="widget_tweet">
	<div class="widget_tweet_img">
		<a href="http://twitter.com/_USERSCREENNAME_"><img src="_USERIMAGE_" /></a></div>
	<div class="widget_tweet_body">
		<a class="widget_screenname" href="http://twitter.com/_USERSCREENNAME_">_USERSCREENNAME_</a> _TWEET_<br />
		<span class="widget_tweet_meta"><a href="http://twitter.com/_USERSCREENNAME_/status/_TWEETID_">_AGO_</a> from _TWEETSOURCE_</span></div>
</div>
{/section}</div>