using UnityEngine;
using UnityEngine.UI; // Import the UI namespace

public class GameManager : MonoBehaviour
{
    public int score = 0;
    public Text scoreText; // Reference to the UI Text component

    void Start()
    {
        // Initialize the score display
        UpdateScoreText();
    }

    public void IncreaseScore()
    {
        score += 1;
        UpdateScoreText(); // Update the UI when the score changes
    }

    void UpdateScoreText()
    {
        scoreText.text = score.ToString();
    }
}
