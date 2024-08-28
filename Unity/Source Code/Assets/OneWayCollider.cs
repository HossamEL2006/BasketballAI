using UnityEngine;

public class OneWayCollider : MonoBehaviour
{
    public Collider2D oneWayCollider;  // The collider that will be toggled
    public string ballTag = "Ball";  // The tag for the ball object

    private Rigidbody2D ballRigidbody;

    void Start()
    {
        GameObject ball = GameObject.FindGameObjectWithTag(ballTag);
        if (ball != null)
        {
            ballRigidbody = ball.GetComponent<Rigidbody2D>();
        }

        if (oneWayCollider == null)
        {
            Debug.LogError("One-way collider is not assigned.");
        }
    }

    void Update()
    {
        if (ballRigidbody != null)
        {
            if (ballRigidbody.velocity.y < 0)  // Ball is moving down
            {
                oneWayCollider.enabled = false;
            }
            else  // Ball is moving up
            {
                oneWayCollider.enabled = true;
            }
        }
    }
}
