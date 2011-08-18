<style type="text/css">
div.widget_tweet a {ldelim} 
	color: #2276BB !important; 
	text-decoration: none !important;
{rdelim}
div.widget_tweet a:hover {ldelim} 
	text-decoration: underline !important; 
{rdelim}
div.widget_tweet {ldelim}
	font-family: 'Lucida Grande', sans-serif;
	font-size: 14px;
	line-height: 16px;
	background-color: white;
	border-bottom: 1px solid #EEEEEE;
	padding: 10px 0 8px;
	position: relative;
{rdelim}
div.widget_tweet span.widget_tweet_meta,
div.widget_tweet span.widget_tweet_meta a {ldelim}
	color: #999999 !important;
	font-size: 11px !important;
{rdelim}
</style><div id="widget">{section name=i loop=$tweets}
<div class="widget_tweet">
	<span style="font-size: 12px;"><span class="widget_tweet_meta"><a href="http://twitter.com/%USERSCREENNAME%/status/%TWEETID%">%AGODAY%</a> by <a href="http://twitter.com/%USERSCREENNAME%">%USERSCREENNAME%</a> </span></span><br />
	%TWEET% <a href="http://twitter.com">Link</a></div>{/section}</div>