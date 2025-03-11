#if TOOLS
using Godot;
using System;
using System.Collections.Generic;

public partial class Building : Area2D
{
	public float Surface { get; set; }
	public string Type { get; set; }
	
	private Polygon2D shape;
	private CollisionPolygon2D collision;
	private Label label;

	public override void _Ready(){
		shape = GetNode<Polygon2D>("Shape");
		collision = GetNode<CollisionPolygon2D>("Collision");
		label = GetNode<Label>("Label");
	}

	public override void _Process(double delta)
	{
		var children = GetChildren();
		if (children.Count > 4) // has at least 1 Dot
		{
			var points = new List<Vector2>();
			var labelPos = Vector2.Zero;
			foreach (var child in children)
			{
				if (child is ColorRect dot)
				{
					var dotPos = dot.Position + new Vector2(dot.Size.X / 2, dot.Size.Y / 2);
					points.Add(dotPos);
					labelPos += dotPos;
				}
			}
			label.Position = labelPos / children.Count;
			label.Text = Name;
			shape.Polygon = points.ToArray();
			collision.Polygon = points.ToArray();
		}
	}
}
#endif
