<?php
// Execute the Python scripts
exec('python data_collection_preprocessing.py');
exec('python topic_modeling.py');
exec('python concept_title_generation.py');

// Redirect to index.php after execution
header('Location: index.php');
exit();
?>
