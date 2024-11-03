<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Function to fetch related articles
function fetch_related_articles($keyword, $limit = 4) {
    $csvFile = 'preprocessed_articles.csv'; // Path to your CSV file
    $related_articles = [];
    
    // Open the CSV file
    if (($handle = fopen($csvFile, 'r')) !== FALSE) {
        $header = fgetcsv($handle); // Read the header

        while (($data = fgetcsv($handle)) !== FALSE) {
            $title = $data[array_search('title', $header)];
            $description = $data[array_search('description', $header)];
            $thumbnail = $data[array_search('thumbnail', $header)];
            $article_link = $data[array_search('article_link', $header)];

            // Check if the title or description contains the keyword
            if (stripos($title, $keyword) !== FALSE || stripos($description, $keyword) !== FALSE) {
                $related_articles[] = [
                    'title' => $title,
                    'thumbnail' => $thumbnail,
                    'link' => $article_link
                ];

                // Limit the number of articles
                if (count($related_articles) >= $limit) {
                    break;
                }
            }
        }
        fclose($handle);
    }
    
    return ['articles' => $related_articles];
}

$article_link = $_GET['link'] ?? '';
$thumbnail_url = $_GET['thumbnail'] ?? '';
$keyword = $_GET['query'] ?? '';

if (!$article_link) {
    echo "No article link provided.";
    exit;
}

// Decode the URL-encoded article link
$article_link = urldecode($article_link);

// Fetch the article content
$rss_content = @file_get_contents($article_link);

if ($rss_content === false) {
    // Try using cURL as an alternative
    $ch = curl_init($article_link);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $rss_content = curl_exec($ch);
    curl_close($ch);

    if ($rss_content === false) {
        echo "Failed to load article content using cURL. Please check the link: $article_link";
        exit;
    }
}

// Parse the content as HTML
$article_dom = new DOMDocument();
libxml_use_internal_errors(true);
$article_dom->loadHTML($rss_content);
libxml_clear_errors();

// Extract the article title and content
$title = '';
$content = '';

// Find title
$title_tags = $article_dom->getElementsByTagName('h1');
if ($title_tags->length > 0) {
    $title = $title_tags->item(0)->textContent;
}

// Find paragraphs
$paragraphs = $article_dom->getElementsByTagName('p');
foreach ($paragraphs as $paragraph) {
    $content .= '<p>' . $paragraph->textContent . '</p>';
}

// Use the thumbnail URL passed from search.php
$image_url = $thumbnail_url; 

// Fetch related articles (limit to 4)
$related_articles = fetch_related_articles($keyword, 4);
?>

<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title><?php echo htmlspecialchars($title); ?></title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            direction: rtl;
            text-align: right;
        }
        header {
            background-color: #007BFF;
            color: #007BFF;
            padding: 20px;
            border-radius: 8px 8px 0 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        header h1 {
            margin: 0;
            font-size: 30px;
            font-weight: bold;
            display: inline-block;
        }
        nav ul {
            list-style-type: none;
            padding: 0;
            margin: 10px 0 0;
            text-align: center;
        }
        nav ul li {
            display: inline;
            margin: 0 10px;
        }
        nav ul li a {
            color: #007BFF;
            text-decoration: none;
            font-size: 18px;
            font-weight: bold;
            transition: color 0.3s;
        }
        nav ul li a:hover {
            color: #a00202;
        }
        .container {
            width: 80%;
            margin: 50px auto;
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 1);
            border-radius: 8px;
        }
        .article img {
            max-width: 100%;
            height: auto;
            display: block;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .related-articles {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 40px;
        }
        .related-article {
            width: 23%; /* Adjusted width */
            text-align: right;
            border: 1px solid #ccc;
            padding: 10px;
            background-color: #fff;
            border-radius: 4px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .related-article img {
            max-width: 100%;
            height: auto;
            display: block;
            margin-bottom: 10px;
        }
        .related-article h2 {
            font-size: 1.2em;
            margin: 0;
        }
        .related-article a {
            text-decoration: none;
            color: #007BFF;
        }
        .related-article a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>البحث في العناوين</h1>
            <nav>
                <ul>
                    <li><a href="index.html">الرئيسية</a></li>
                    <li><a href="about.html">معلومات عنا</a></li>
                    <li><a href="contact.html">اتصل بنا</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <div class="container">
    <div class="article">
        <h1><?php echo htmlspecialchars($title); ?></h1>
        <img src="<?php echo htmlspecialchars($image_url); ?>" alt="<?php echo htmlspecialchars($title); ?>">
        <div><?php echo $content; ?></div>
    </div>

    <h2>مقالات ذات صلة</h2>
    <div class="related-articles">
        <?php foreach ($related_articles['articles'] as $related_article): ?>
            <div class="related-article">
                <?php if (!empty($related_article['thumbnail'])): ?>
                    <img src="<?php echo htmlspecialchars($related_article['thumbnail']); ?>" alt="<?php echo htmlspecialchars($related_article['title']); ?>">
                <?php endif; ?>
                <h2><?php echo html_entity_decode(htmlspecialchars($related_article['title'])); ?></h2>
                <a href="read_more.php?link=<?php echo urlencode($related_article['link'] ?? ''); ?>&thumbnail=<?php echo urlencode($related_article['thumbnail'] ?? ''); ?>&query=<?php echo urlencode($keyword ?? ''); ?>">اقرأ المزيد</a>
            </div>
        <?php endforeach; ?>
    </div>
</div>

</body>
</html>
