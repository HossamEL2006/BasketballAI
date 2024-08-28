using UnityEngine;

public class ResetTrigger : MonoBehaviour
{
    public GameObject scoringTrigger; // Reference to the primary scoring trigger

    void OnTriggerEnter2D(Collider2D other) // Use OnTriggerEnter for 3D
    {
        if (other.CompareTag("Ball"))
        {
            // Reactivate the scoring trigger
            scoringTrigger.SetActive(true);
        }
    }
}
