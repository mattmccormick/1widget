<?php

function smarty_prefilter_twitter($source, &$smarty)
{
	$dict = array(
		'%ICON%' => '{$feeds[i]->getIcon()}',
		'%IMAGE%' => '{$feeds[i]->image}',
		'%TEXT%' => '{$feeds[i]->text|truncate:200}',
		'%LINK%' => '{$feeds[i]->link}',
		'%SOURCE%' => '{$feeds[i]->source}',
		'%SOURCE_DESCRIPTION%' => '{$feeds[i]->source_description}',
		'%SOURCE_URL%' => '{$feeds[i]->source_url}',

		// RSS specific

		'%RSS_CONTENT%' => '{$feeds[i]->rss_content}',
		'%RSS_TITLE%' => '{$feeds[i]->rss_title}',

		// Twitter specific
		'%TWITTER_FULLNAME%' => '{$feeds[i]->twitter_source_name}',
		'%TWITTER_LOCATION%' => '{$feeds[i]->twitter_source_location}',
		'%TWITTER_ID%' => '{$feeds[i]->twitter_id}',
		'%TWITTER_SOURCE%' => '{$feeds[i]->twitter_source}',

		// Date/Time specific
		'%AGODAY%' => '{$feeds[i]->datetime|ago}',
		'%YYYY%' => '{$feeds[i]->datetime|date_format:"%Y"}',
		'%YY%' => '{$feeds[i]->datetime|date_format:"%y"}',
		'%MM%' => '{$feeds[i]->datetime|date_format:"%m"}',
		'%MONTHFULL%' => '{$feeds[i]->datetime|date_format:"%B"}',
		'%MON%' => '{$feeds[i]->datetime|date_format:"%b"}',
		'%DD%' => '{$feeds[i]->datetime|date_format:"%e"}',
		'%D%' => '{$feeds[i]->datetime|date_format:"%d"}',
		'%DAYFULL%' => '{$feeds[i]->datetime|date_format:"%A"}',
		'%DAY%' => '{$feeds[i]->datetime|date_format:"%a"}',
		'%HH24%' => '{$feeds[i]->datetime|date_format:"%H"}',
		'%HH12%' => '{$feeds[i]->datetime|date_format:"%I"}',
		'%H24%' => '{$feeds[i]->datetime|date_format:"%k"}',
		'%H12%' => '{$feeds[i]->datetime|date_format:"%l"}',
		'%MIN%' => '{$feeds[i]->datetime|date_format:"%M"}',
		'%SS%' => '{$feeds[i]->datetime|date_format:"%S"}',
		'%AMPM%' => '{$feeds[i]->datetime|date_format:"$p"}'
	);

	return strtr($source, $dict);
}
