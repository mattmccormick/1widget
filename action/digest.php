<?php

include '/home/widget/lib/class.digest.php';

$digest = new Digest();
$digest->update($argv[1]);