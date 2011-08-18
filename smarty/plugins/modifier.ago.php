<?php

define("SECOND", 1);
define("MINUTE", 60 * SECOND);
define("HOUR", 60 * MINUTE);
define("DAY", 24 * HOUR);
define("MONTH", 30 * DAY);

function smarty_modifier_ago($time) {
	if (is_numeric($time)) {
		$t = $time;
	} else {
		$t = strtotime($time);
	}
	
    $delta = time() - $t;

    if ($delta < 1 * MINUTE) {
        return $delta == 1 ? "one second ago" : $delta . " seconds ago";
    } else if ($delta < 2 * MINUTE) {
		return "a minute ago";
    } else if ($delta < 45 * MINUTE) {
        return floor($delta / MINUTE) . " minutes ago";
    } else if ($delta < 90 * MINUTE) {
      	return "about an hour ago";
    } else if ($delta < 24 * HOUR) {
      	return 'about ' . floor($delta / HOUR) . " hours ago";
    } else {
    	return date('g:i A M jS', $t);
    }
}