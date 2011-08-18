<?php

include '/home/widget/lib/db.php';
require_once '/home/widget/lib/twitterOAuth.php';

class Feed
{
    private $db;

    public function __construct()
    {
        $this->db = new Db();
    }

    public function updateAll()
    {
        $feeds = $this->db->getAllFeeds();

        // enter own keys here
        $oauth = new TwitterOAuth('OAUTH_TOKEN', 'OAUTH_TOKEN_SECRET');

        for ($i = 0; $i < count($feeds); $i++) {
            $filename = "{$feeds[$i]->username}.json";

            $out = $oauth->oAuthRequest("http://twitter.com/statuses/user_timeline/{$filename}");

            $file = "/home/widget/twitter/sources/{$filename}";
            file_put_contents($file, $out, LOCK_EX);

            $rate_limit = $oauth->oAuthRequest('http://twitter.com/account/rate_limit_status.json');
            print_r(json_decode($rate_limit));
        }


        $ch = curl_init();

        $rss_feeds = $this->db->getAllRss();

        foreach ($rss_feeds as $rss)
        {
            curl_setopt($ch, CURLOPT_URL, $rss->url);
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

            $out = curl_exec($ch);

            $file = "/home/widget/twitter/sources/rss/{$rss->id}.rss";
            file_put_contents($file, $out, LOCK_EX);
        }

        curl_close($ch);
    }

    public function removeUnused()
    {
        $this->db->removeUnusedFeeds();
    }
}
