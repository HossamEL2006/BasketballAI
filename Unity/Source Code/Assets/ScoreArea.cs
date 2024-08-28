using UnityEngine;

public class ScoreArea : MonoBehaviour
{
    public GameManager gameManager;

    void OnTriggerEnter2D(Collider2D other) // Use OnTriggerEnter for 3D
    {
        if (other.CompareTag("Ball"))
        {
            // Increase the shared score
            gameManager.IncreaseScore();

            // Deactivate this scoring trigger
            gameObject.SetActive(false);
        }
    }
}
