<?php
foreach(stream_get_wrappers() as &$stream) {
  stream_wrapper_unregister($stream);
}

stream_wrapper_restore('file');
stream_wrapper_restore('http');
stream_wrapper_restore('https');
?>
