<?php
header('Content-Type: text/html; charset=utf-8');
if (isset($_GET['query'])) {
    $query = $_GET['query'];
    $csvFile = 'articles_with_titles.csv';
    $searchResultsFile = 'search_results.csv';

    // Initialize an empty results array
    $results = [];

    // Open the CSV file with UTF-8 encoding
    if (($handle = fopen($csvFile, 'r')) !== FALSE) {
        // Read the header
        $header = fgetcsv($handle);

        // Read each row and check if the query is in the title or description
        while (($data = fgetcsv($handle)) !== FALSE) {
            $title = html_entity_decode($data[array_search('concept_title', $header)], ENT_QUOTES, 'UTF-8');
            $description = html_entity_decode($data[array_search('description', $header)], ENT_QUOTES, 'UTF-8');
            $thumbnail = html_entity_decode($data[array_search('thumbnail', $header)], ENT_QUOTES, 'UTF-8');
            $article_link = html_entity_decode($data[array_search('article_link', $header)], ENT_QUOTES, 'UTF-8');

            // Check if the query is present in the title or description
            if (stripos($title, $query) !== FALSE || stripos($description, $query) !== FALSE) {
                $results[] = [
                    'title' => $title,
                    'description' => $description,
                    'thumbnail' => $thumbnail,
                    'article_link' => $article_link
                ];
            }
        }
        fclose($handle);
    }

    // Save the search results to a CSV file
    if (($outputHandle = fopen($searchResultsFile, 'w')) !== FALSE) {
        fputcsv($outputHandle, ['title', 'description', 'thumbnail', 'article_link']);
        foreach ($results as $result) {
            fputcsv($outputHandle, $result);
        }
        fclose($outputHandle);
    } else {
        echo "Error: Unable to open $searchResultsFile for writing.";
        exit;
    }

    // Run the article similarity search script
    exec("python article_similarity_search.py $searchResultsFile");

    // Run the generate similarity JSON script
    exec("python generate_similarity_json.py");

    // Pagination logic
    $results_per_page = 8;
    $total_results = count($results);
    $total_pages = ceil($total_results / $results_per_page);
    $current_page = isset($_GET['page']) ? (int)$_GET['page'] : 1;

    if ($current_page > $total_pages) {
        $current_page = $total_pages;
    } elseif ($current_page < 1) {
        $current_page = 1;
    }

    $start_index = ($current_page - 1) * $results_per_page;
    $paginated_results = array_slice($results, $start_index, $results_per_page);

    // Output HTML
    echo "<!DOCTYPE html>";
    echo "<html lang='ar'>";
    echo "<head>";
    echo "<meta charset='UTF-8'>";
    echo "<meta name='viewport' content='width=device-width, initial-scale=1.0'>";
    echo "<title>نتائج البحث</title>";
    echo "<style>";
    echo "body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; direction: rtl; text-align: right; }";
    echo ".container { width: 80%; margin: 50px auto; background-color: #fff; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 1); border-radius: 8px; }";
    echo "header { background-color: #007BFF; color: #007BFF; padding: 20px; border-radius: 8px 8px 0 0; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); position: relative; }";
    echo "header h1 { margin: 0; font-size: 30px; display: inline-block; font-weight: bold;}";
    echo "nav ul { list-style-type: none; padding: 0; margin: 10px 0 0; text-align: center; }";
    echo "nav ul li { display: inline; margin: 0 10px; }";
    echo "nav ul li a { color: #007BFF; text-decoration: none; font-size: 18px; transition: color 0.3s; font-weight: bold; }";
    echo "nav ul li a:hover { color: #a00202; }";
    echo ".grid-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }";
    echo ".grid-item { border: 1px solid #ccc; padding: 10px; border-radius: 4px; }";
    echo ".thumbnail { max-width: 100%; height: auto; }";
    echo ".read-more { display: block; margin-top: 10px; padding: 10px; text-align: center; background-color: #007BFF; color: #fff; text-decoration: none; border-radius: 4px; }";
    echo ".read-more:hover { background-color: #0056b3; }";
    echo ".pagination { text-align: center; margin-top: 20px; }";
    echo ".pagination a { display: inline-block; padding: 8px 16px; background-color: #f2f2f2; color: #333; text-decoration: none; border: 1px solid #ccc; border-radius: 4px; margin-right: 5px; }";
    echo ".pagination a.active { background-color: #0056b3; color: white; border: 1px solid #4CAF50; }";
    echo ".pagination a:hover { background-color: #ddd; }";
    echo "</style>";
    echo "</head>";
    echo "<body>";
    echo "<header>";
    echo "<div class='container'>";
    echo "<h1>البحث في العناوين</h1>";
    echo "<nav>";
    echo "<ul>";
    echo "<li><a href='index.html'>الرئيسية</a></li>";
    echo "<li><a href='about.html'>معلومات عنا</a></li>";
    echo "<li><a href='contact.html'>اتصل بنا</a></li>";
    echo "<li><a href='visualize_topics.html'>تصور الموضوعات</a></li>";
    echo "</ul>";
    echo "</nav>";
    echo "</div>";
    echo "</header>";
    echo "<div class='container'>";
    echo "<h1>نتائج البحث عن '" . htmlspecialchars($query, ENT_QUOTES, 'UTF-8') . "'</h1>";

    if (empty($results)) {
        echo "<p>لم يتم العثور على نتائج.</p>";
    } else {
        echo "<div class='grid-container'>";
        foreach ($paginated_results as $result) {
            echo "<div class='grid-item'>";
            if (!empty($result['thumbnail'])) {
                echo "<img src='" . htmlspecialchars($result['thumbnail'], ENT_QUOTES, 'UTF-8') . "' class='thumbnail' alt='Thumbnail'>";
            }
            echo "<h2>" . htmlspecialchars($result['title'], ENT_QUOTES, 'UTF-8') . "</h2>";
            echo "<p>" . htmlspecialchars($result['description'], ENT_QUOTES, 'UTF-8') . "</p>";
            echo "<a href='read_more.php?link=" . urlencode($result['article_link']) . "&thumbnail=" . urlencode($result['thumbnail']) . "&query=" . urlencode($query) . "' class='read-more'>اقرأ المزيد</a>";
            echo "</div>";
        }
        echo "</div>";

        echo "<div class='pagination'>";
        if ($current_page > 1) {
            echo "<a href='?query=" . urlencode($query) . "&page=" . ($current_page - 1) . "'>السابق</a>";
        }
        echo "<a class='active'>$current_page</a>";
        if ($current_page < $total_pages) {
            echo "<a href='?query=" . urlencode($query) . "&page=" . ($current_page + 1) . "'>التالي</a>";
        }
        echo "</div>";
    }

    echo "</div>";
    echo "</body>";
    echo "</html>";
}
?>
