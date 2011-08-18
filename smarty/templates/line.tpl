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
		/* Single Line */
		google_ad_slot = "8862318564";
		google_ad_width = 200;
		google_ad_height = 90;
		//-->
		</script>
		<script type="text/javascript"
		src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
		</script>
	</div>
	{/if}
	<div class="widget_tweet">{$feeds[i]->text|truncate:200}</div>
	{/section}
</div>