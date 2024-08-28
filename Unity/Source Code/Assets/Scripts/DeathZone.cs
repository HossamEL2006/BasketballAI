using UnityEngine;
using UnityEngine.SceneManagement;

public class DeathZone : MonoBehaviour
{
    // Reference to the sprite GameObject
    public GameObject gameOverSprite;
    private bool gameOver = false;

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Ball"))
        {
            // Toggle the sprite on
            gameOverSprite.SetActive(true);

            // Freeze the game
            Time.timeScale = 0f;

            // Enable game restart
            gameOver = true;
        }
    }

    void Update()
    {
        // Check for mouse click to restart the level
        if (Input.GetMouseButtonDown(0) && gameOver)
        {
            RestartLevel();
        }
    }

    void RestartLevel()
    {
        // Unfreeze the game and restart the level
        Time.timeScale = 1f;
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }
}
