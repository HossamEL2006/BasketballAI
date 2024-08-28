using UnityEngine;

public class Player : MonoBehaviour
{
    public float forceIntensity = 10f; // Intensity of the force
    private Rigidbody2D rb;

    private bool gamePaused = true;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();

        // Pause the game at the start
        Time.timeScale = 0f;
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0)) // If left mouse button is pressed
        {
            if (gamePaused) // Check for the first left-click
            {
                ResumeGame();
            } else
			{
                // Get the mouse position in world space
                Vector3 mousePosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
                mousePosition.z = 0; // Set z to 0 since we're working in 2D

                // Calculate the direction from the ball to the mouse
                Vector2 direction = mousePosition - transform.position;
                direction.Normalize(); // Normalize the direction to get a unit vector

                // Calculate the new velocity to apply
                Vector2 newVelocity = direction * forceIntensity;

                // Cancel all previous forces by directly setting the velocity
                rb.velocity = newVelocity;
            }
        }
    }

    void ResumeGame()
    {
        // Unpause the game
        Time.timeScale = 1f;
        gamePaused = false;
    }
}
