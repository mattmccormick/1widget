<?php

include_once '/home/widget/lib/db.php';
include_once '/home/widget/lib/simplepie.inc';
include_once '/home/widget/lib/class.widget_item.php';

class Digest
{
	const GROUP_FREE = 1;
	const GROUP_SMALL = 2;
	const GROUP_MULTI = 3;
	const GROUP_PREMIUM = 4;

	private $db;

	public function __construct()
	{
		$this->db = new Db();
	}

	public function updatePackage($group_id)
	{
		$digests = $this->db->getByPackage($group_id);

		$free = false;
		if ($group_id == 1) {
			$free = true;
		}

		foreach ($digests as $digest) {
			$this->updateDigest($digest, $free);
		}
	}

	public function update($id)
	{
		$digest = $this->db->getDigest($id);

		if (!$digest) {
			return;
		}

		$this->updateDigest($digest, $this->db->isUserFree($digest->user_id));
	}

	private function updateDigest(stdClass $digest, $free = false)
	{
		require_once '/usr/local/lib/php/Smarty/Smarty.class.php';
		$smarty = new Smarty();
		$smarty->template_dir = '/home/widget/smarty/templates';
		$smarty->compile_dir = '/home/widget/smarty/templates_c';
		$smarty->cache_dir = '/home/widget/smarty/cache';
		$smarty->config_dir = '/home/widget/smarty/configs';
		$smarty->plugins_dir[] = '/home/widget/smarty/plugins';
		$smarty->force_compile = true;
		$smarty->load_filter('pre', 'twitter');

		$template = $this->db->getTemplate($digest->template_id);

		$keywords = array();
		if ($digest->keywords) {
			$keywords = explode(' OR ', $digest->keywords);
		}

		$tweets = $this->getTweets($digest, $keywords);
		$rss = $this->getRss($digest, $keywords);

		$feeds = array_merge($tweets, $rss);

		usort($feeds, array('WidgetItem', 'sort'));

		$final = array_slice($feeds, 0, $digest->items);

		if ($free) {
			$ad_pos = rand(0, count($final) - 1);
			$smarty->assign('ad_pos', $ad_pos);
		}

		$smarty->assign('free', $free);
		$smarty->assign_by_ref('feeds', $final);
		$html = $smarty->fetch($template->tpl);

		//TODO: will need to handle encoding errors
		// could have select box for encoding
		$filename = "/home/widget/public_html/twitter/{$digest->digest_id}.html";
		file_put_contents($filename, $html);
		chmod($filename, 0666);
	}

	/**
	 * Returns an array of tweets
	 * @param stdClass $digest
	 * @param array $keywords
	 * @return array WidgetItem
	 */
	private function getTweets(stdClass $digest, array $keywords)
	{
		$user_tweets = $this->db->getFeeds($digest->id);

		$feeds = array();

		foreach ($user_tweets as $tweets) {
			$json = file_get_contents("/home/widget/twitter/sources/{$tweets->username}.json");
			if (!$json) {
				continue;
			}

			$tweets = json_decode($json);

			foreach ($tweets as $tweet) {
				$item = new WidgetItem($tweet);
				$this->addItem($item, $feeds, $keywords);
			}
		}

		return $feeds;
	}

	/**
	 * Return an array of RSS items
	 * @param stdClass $digest
	 * @param array $keywords
	 * @return array WidgetItem
	 */
	private function getRss(stdClass $digest, array $keywords)
	{
		$rss_feeds = $this->db->getRssFeeds($digest->id);

		$feeds = array();

		if (!$rss_feeds) {
			return $feeds;
		}

		$urls = array();
		foreach ($rss_feeds as $rss) {
			$urls[] = "/home/widget/twitter/sources/rss/{$rss->id}.rss";
		}

		$feed = new SimplePie();
		$feed->set_feed_url($urls);
		$feed->set_autodiscovery_level(SIMPLEPIE_LOCATOR_NONE);
		$feed->set_item_limit($digest->items);	// set to number of items for Digest
		$feed->init();

		$max = $feed->get_item_quantity($digest->items);	// same as above

		for ($i = 0; $i < $max; $i++) {
			$item = new WidgetItem($feed->get_item($i));
			$this->addItem($item, $feeds, $keywords);
		}

		return $feeds;
	}

	/**
	 * Adds the Item to the array if the item contains the keywords if specified
	 * @param WidgetItem $item
	 * @param array $feeds
	 * @param array $keywords
	 */
	private function addItem(WidgetItem $item, array &$feeds, array $keywords)
	{
		if (!empty($keywords)) {
			foreach ($keywords as $keyword) {
				if (stripos($item->text, $keyword) !== false) {
					$feeds[] = $item;
					return;
				}
			}
		} else {
			$feeds[] = $item;
		}
	}
}
