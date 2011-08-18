{literal}
<style type="text/css">

div#widget {
	font-family: 'Lucida Grande', sans-serif;
	font-size: 14px;
	line-height: 16px;
	background-color: white;
}

div.widget_tweet a {
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

div.widget_tweet span.widget_tweet_meta,
div.widget_tweet span.widget_tweet_meta a {
	color: #999999;
	font-size: 11px;
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
		<span class="widget_tweet_meta"><a href="{$feeds[i]->link}">{$feeds[i]->datetime|ago}</a>
		by
		<a href="{$feeds[i]->source_url}">{$feeds[i]->source}</a></span><br />
		{$feeds[i]->text|truncate:200}
	</div>
	{/section}
</div>