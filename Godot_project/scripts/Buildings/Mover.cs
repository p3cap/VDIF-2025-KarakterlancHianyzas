using Godot;
using System;

public partial class Mover : ColorRect{
	private bool isDragging = false;

	public override void _Input(InputEvent @event){
		if (@event is InputEventMouseButton mouseEvent){
			if (mouseEvent.ButtonIndex == MouseButton.Left){
				if (mouseEvent.Pressed){ isDragging = true; }
				else{ isDragging = false; }
			}
		}

		if (isDragging){
			Position = GetGlobalMousePosition();
		}
	}
}
