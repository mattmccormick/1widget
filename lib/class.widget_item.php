<?php

require_once '/home/widget/lib/simplepie.inc';

class WidgetItem
{
	public function __construct($item)
	{
		if (is_a($item, 'SimplePie_Item')) {
			$this->type = 'rss';
			$this->setRss($item);
		} else {
			$this->type = 'twitter';
			$this->setTwitter($item);
		}
	}

	public function getIcon()
	{
		return '<img src="http://www.1widget.com/media/img/' . $this->type
			. '.gif" width="19" height="19" class="widget_icon" alt="' . $this->type . '" />';
	}

	public function getImage()
	{
		$html = '';
		$src = $this->image;
		if ($src) {
			$html = '<img src="' . $src . '" alt="' . htmlspecialchars($this->source) . '" />';
		}

		return $html;
	}

	private function setRss(SimplePie_Item $item)
	{
		$this->text = trim($this->linkify(strip_tags($item->get_description())));
		$this->datetime = $item->get_date();
		$this->link = $item->get_link();

		$feed = $item->get_feed();
		$this->image = $feed->get_image_url();
		$this->source = $feed->get_title();
		$this->source_url = $feed->get_link();
		$this->source_description = $feed->get_description();

		// Extra RSS specific information
		$this->rss_content = $this->linkify(strip_tags($item->get_content()));
		$this->rss_title = strip_tags($item->get_title());
	}

	private function setTwitter(stdClass $item)
	{
		$this->text = $this->linkifyTwitter($item->text);
		$this->datetime = $item->created_at;
		$this->link = "http://twitter.com/{$item->user->screen_name}/status/{$item->id}";
		$this->image = $item->user->profile_image_url;
		$this->source = $item->user->screen_name;
		$this->source_url = "http://twitter.com/{$item->user->screen_name}";
		$this->source_description = $item->user->description;

		// Extra Twitter specific information
		$this->twitter_source_name = $item->user->name;
		$this->twitter_id = $item->id;
		$this->twitter_source = str_replace('href="/', 'href="http://twitter.com/',
			$item->source);
		$this->twitter_source_location = $item->user->location;
	}

	private function linkify($text)
	{
		return preg_replace('/(http:\/\/[\S]+)/', '<a href="\\1">\\1</a>', $text);
	}

	private function linkifyTwitter($text)
	{
		$result = $this->linkify($text);
		return preg_replace('/(@([\S]+))/',
			'@<a href="http://twitter.com/\\2">\\2</a>', $result);
	}

	public static function sort(WidgetItem $a, WidgetItem $b)
	{
		return date('U', strtotime($a->datetime))
			<= date('U', strtotime($b->datetime));
	}
}