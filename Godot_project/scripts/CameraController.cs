using Godot;
//kamera irányítása
public partial class CameraController : Camera2D
{
	private float _zoomSpeed = 0.1f;
	private float _minZoom = 0.5f;
	private float _maxZoom = 2.0f;

	private bool _isDragging = false;
	private Vector2 _lastMousePosition = Vector2.Zero;

	public override void _Input(InputEvent @event){
		if (@event is InputEventMouseButton mouseEvent){
			if (mouseEvent.ButtonIndex == MouseButton.WheelUp && Zoom.X > _minZoom){
				Zoom -= new Vector2(_zoomSpeed, _zoomSpeed);
			}
			else if (mouseEvent.ButtonIndex == MouseButton.WheelDown && Zoom.X < _maxZoom){
				Zoom += new Vector2(_zoomSpeed, _zoomSpeed);
			}
			else if (mouseEvent.ButtonIndex == MouseButton.Middle){
				if (mouseEvent.Pressed){
					_isDragging = true;
					_lastMousePosition = GetGlobalMousePosition();
				}
				else{ _isDragging = false; }
			}
		}
		else if (@event is InputEventMouseMotion mouseMotionEvent && _isDragging){
			Vector2 mouseDelta = GetGlobalMousePosition() - _lastMousePosition;
			Position -= mouseDelta;
			_lastMousePosition = GetGlobalMousePosition();
		}
	}
}
