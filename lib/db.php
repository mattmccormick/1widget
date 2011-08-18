<?php

class Db
{
	private $dbh;

	public function __construct()
	{
		try {
			$this->dbh = new PDO('mysql:host=localhost;dbname=widget_twitter',
				'widget_widget', 'q3u(Qe3(xHfV');
		} catch (Exception $e) {
			error_log($e->getMessage(), 3, '/home/widget/action/error_log');
		}
	}

	/**
	 * Returns all Digests for the specified Package
	 * @param int $group_id
	 */
	public function getByPackage($group_id)
	{
		$sql = 'SELECT d.* FROM control_digest d, auth_user_groups ug
			WHERE d.user_id = ug.user_id
			AND ug.group_id = ?';
		$stmt = $this->dbh->prepare($sql);
		$stmt->execute(array($group_id));

		return $stmt->fetchAll(PDO::FETCH_OBJ);
	}

	/**
	 * Returns the digest by ID
	 * @param int $id
	 * @return stdClass
	 */
	public function getDigest($id)
	{
		$sql = 'SELECT * FROM control_digest WHERE id = ?';
		$stmt = $this->dbh->prepare($sql);
		$stmt->execute(array($id));

		return $stmt->fetchObject();
	}

	public function isUserFree($user_id)
	{
		$sql = 'SELECT group_id FROM auth_user_groups WHERE user_id = ?';
		$stmt = $this->dbh->prepare($sql);
		$stmt->execute(array($user_id));

		$group = $stmt->fetchColumn();

		return $group == 1;
	}

	/**
	 * Get feeds by digest ID
	 * @param int $id_digest
	 * @return stdClass
	 */
	public function getFeeds($id_digest)
	{
		$sql = 'SELECT f.username
			FROM control_feed f, control_digest_feeds df
			WHERE df.digest_id = ?
			AND df.feed_id = f.id';
		$stmt = $this->dbh->prepare($sql);
		$stmt->execute(array($id_digest));

		return $stmt->fetchAll(PDO::FETCH_OBJ);
	}

	/**
	 * Get RSS feeds by digest ID
	 * @param int $id_digest
	 * @return array stdClass
	 */
	public function getRssFeeds($id_digest)
	{
		$sql = 'SELECT r . *
			FROM control_rss r, control_digest_rss dr
			WHERE dr.digest_id = ?
			AND dr.rss_id = r.id';
		$stmt = $this->dbh->prepare($sql);
		$stmt->execute(array($id_digest));

		return $stmt->fetchAll(PDO::FETCH_OBJ);
	}

	/**
	 * Get all feeds
	 * @return array of stdClass
	 */
	public function getAllFeeds()
	{
		$sql = 'SELECT username FROM control_feed';
		$stmt = $this->dbh->prepare($sql);
		$stmt->execute();

		return $stmt->fetchAll(PDO::FETCH_OBJ);
	}

	public function getAllTokens()
	{
		$sql = 'SELECT token, token_secret FROM control_oauth';
		$stmt = $this->dbh->prepare($sql);
		$stmt->execute();

		return $stmt->fetchAll(PDO::FETCH_OBJ);
	}

	public function getAllRss()
	{
		$sql = 'SELECT * FROM control_rss';
		$stmt = $this->dbh->prepare($sql);
		$stmt->execute();

		return $stmt->fetchAll(PDO::FETCH_OBJ);
	}

	/**
	 * Removes feeds that are not being used in digests
	 * @return int number of rows deleted
	 */
	public function removeUnusedFeeds()
	{
		$sql = 'DELETE FROM control_feed WHERE id NOT IN (
					SELECT DISTINCT (feed_id)
					FROM  `control_digest_feeds`
				)';
		$this->dbh->exec($sql);

		$sql_rss = 'DELETE FROM  `control_rss`
			WHERE id NOT IN (
				SELECT DISTINCT (rss_id) FROM control_digest_rss
			)';
		$this->dbh->exec($sql_rss);
	}

	public function getTemplate($id)
	{
		$sql = 'SELECT * FROM control_template WHERE id = ?';
		$stmt = $this->dbh->prepare($sql);
		$stmt->execute(array($id));

		return $stmt->fetchObject();
	}
}