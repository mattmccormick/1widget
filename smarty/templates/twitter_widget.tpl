{literal}
<style type="text/css">

div#widget {
	font-family: "lucida grande",lucida,tahoma,helvetica,arial,sans-serif !important;
	font-size: 12px;
	background-color: black;
	color: white;
}

div#widget a:hover {
	text-decoration: underline;
}

div.widget_tweet a {
	color: #4AED05;
	text-decoration: none;
}

div.widget_tweet {
	border-bottom: 1px dotted #DDDDDD;
	padding: 6px 8px;
}

div.widget_tweet span.widget_tweet_meta,
div.widget_tweet span.widget_tweet_meta a {
	color: white;
	font-size: 9px;
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
		/* Twitter Widget */
		google_ad_slot = "8788360163";
		google_ad_width = 234;
		google_ad_height = 60;
		//-->
		</script>
		<script type="text/javascript"
		src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
		</script>
	</div>
	{/if}
	<div class="widget_tweet">
		{$feeds[i]->text|truncate:200}<br />
		<span class="widget_tweet_meta"><a href="{$feeds[i]->link}">{$feeds[i]->datetime|ago}</a>
		by
		<a href="{$feeds[i]->source_url}">{$feeds[i]->source}</a></span>
	</div>
	{/section}
</div>