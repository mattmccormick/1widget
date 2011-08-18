<style type="text/css">
div.widget_tweet a {ldelim}
	color: #2276BB !important;
	text-decoration: none !important;
	width: 700px;
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
.style1 {ldelim}font-family: Arial, Helvetica, sans-serif, Chiller{rdelim}
</style><div id="widget">{section name=i loop=$feeds}
<div class="widget_tweet">
	<p>
		<span style="width-size: 700px"><span style="font-size: 14px"><span style="font-family: arial, helvetica, sans-serif"><span class="widget_tweet_meta style1"><a href="%LINK%">%AGODAY%</a> by <a href="%SOURCE%">%SOURCE%</a> </span><br />
		</span></span><span style="font-size: 10px">%TEXT%</span></p>
</div>{/section}</div>