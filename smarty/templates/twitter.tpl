{literal}
<style type="text/css">

div#widget {
	font-family: 'Lucida Grande', sans-serif;
	font-size: 14px;
	line-height: 16px;
	background-color: white;
}

div.widget_tweet_body a {
	color: #2277BB;
	text-decoration: none;
}

div#widget a:hover {
	text-decoration: underline;
}

div.widget_tweet {
	border-bottom: 1px solid #EEEEEE;
	padding: 10px 0 8px;
	position: relative;
	overflow: hidden;
}

div.widget_tweet:hover {
	background-color: #F7F7F7;
}

div.widget_tweet_img {
	height: 50px;
	width: 50px;
	float: left;
}

div.widget_tweet_img img {
	border: none;
	max-height: 48px;
	max-width: 48px;
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

div.widget_tweet_body span.widget_tweet_meta {
	float: left;
}

div.widget_tweet_body img.widget_icon {
	float: right;
}

</style>
{/literal}

<div id="widget">
	{if $free}
	<a href="http://www.1widget.com"><img src="http://www.1widget.com/media/img/logo_sm.png" width="120" height="38" border="0" alt="1widget" /></a>
	{/if}
	{section name=i loop=$feeds}
	{if $free && %i.index% eq $ad_pos}
	<div class="widget_tweet">
	<script type="text/javascript"><!--
		google_ad_client = "pub-4299371897226000";
		/* Twitter Default */
		google_ad_slot = "4586530447";
		google_ad_width = 234;
		google_ad_height = 60;
	//-->
	</script>
	<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
	</div>
	{/if}
	<div class="widget_tweet">
		<div class="widget_tweet_img">
			<a href="{$feeds[i]->source_url}">{$feeds[i]->getImage()}</a>
		</div>
		<div class="widget_tweet_body">
			<a href="{$feeds[i]->source_url}" class="widget_screenname">{$feeds[i]->source}</a>
			{$feeds[i]->text|truncate:200}<br />
			<span class="widget_tweet_meta"><a href="{$feeds[i]->link}">{$feeds[i]->datetime|ago}</a></span>
			{$feeds[i]->getIcon()}
		</div>
	</div>
	{/section}
</div>