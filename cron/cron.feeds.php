#!/usr/bin/php
<?php

include '/home/widget/lib/class.feed.php';

$feed = new Feed();

$feed->removeUnused();
$feed->updateAll();

print_r(json_decode(file_get_contents('http://twitter.com/account/rate_limit_status.json')));