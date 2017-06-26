# -*- coding: utf-8 -*-


def test_vispy():
    from vispy.plot import Fig
    fig = Fig()
    ax = fig[0, 0]
    ax.plot([[0, 1], [1, 2]])


def qt_hello_world():
    # example taken from http://fr.wikibooks.org/wiki/PyQt/Premier_exemple_:_Hello_World_!

    import sys
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
    from PyQt5.QtCore import QSize

    class HelloWindow(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)

            self.setMinimumSize(QSize(640, 480))
            self.setWindowTitle("Hello world")

            # centralWidget = QWidget(self)
            # self.setCentralWidget(centralWidget)
            #
            # gridLayout = QGridLayout(self)
            # centralWidget.setLayout(gridLayout)

            title = QLabel("Hello World from PyQt", self)
            title.setAlignment(QtCore.Qt.AlignCenter)
            # gridLayout.addWidget(title, 0, 0)
            self.setCentralWidget(title)

    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit(app.exec_())


def test_native():

    import vispy
    vispy.test()


def test_signal():


    """
    Multiple real-time digital signals with GLSL-based clipping.
    """

    import sys
    print(sys.path)

    from vispy import gloo
    from vispy import app
    import numpy as np
    import math

    # Number of cols and rows in the table.
    nrows = 16
    ncols = 20

    # Number of signals.
    m = nrows*ncols

    # Number of samples per signal.
    n = 1000

    # Various signal amplitudes.
    amplitudes = .1 + .2 * np.random.rand(m, 1).astype(np.float32)

    # Generate the signals as a (m, n) array.
    y = amplitudes * np.random.randn(m, n).astype(np.float32)

    # Color of each vertex (TODO: make it more efficient by using a GLSL-based
    # color map and the index).
    color = np.repeat(np.random.uniform(size=(m, 3), low=.5, high=.9),
                      n, axis=0).astype(np.float32)

    # Signal 2D index of each vertex (row and col) and x-index (sample index
    # within each signal).
    index = np.c_[np.repeat(np.repeat(np.arange(ncols), nrows), n),
                  np.repeat(np.tile(np.arange(nrows), ncols), n),
                  np.tile(np.arange(n), m)].astype(np.float32)

    VERT_SHADER = """
    #version 120
    // y coordinate of the position.
    attribute float a_position;
    // row, col, and time index.
    attribute vec3 a_index;
    varying vec3 v_index;
    // 2D scaling factor (zooming).
    uniform vec2 u_scale;
    // Size of the table.
    uniform vec2 u_size;
    // Number of samples per signal.
    uniform float u_n;
    // Color.
    attribute vec3 a_color;
    varying vec4 v_color;
    // Varying variables used for clipping in the fragment shader.
    varying vec2 v_position;
    varying vec4 v_ab;
    void main() {
        float nrows = u_size.x;
        float ncols = u_size.y;
        // Compute the x coordinate from the time index.
        float x = -1 + 2*a_index.z / (u_n-1);
        vec2 position = vec2(x - (1 - 1 / u_scale.x), a_position);
        // Find the affine transformation for the subplots.
        vec2 a = vec2(1./ncols, 1./nrows)*.9;
        vec2 b = vec2(-1 + 2*(a_index.x+.5) / ncols,
                      -1 + 2*(a_index.y+.5) / nrows);
        // Apply the static subplot transformation + scaling.
        gl_Position = vec4(a*u_scale*position+b, 0.0, 1.0);
        v_color = vec4(a_color, 1.);
        v_index = a_index;
        // For clipping test in the fragment shader.
        v_position = gl_Position.xy;
        v_ab = vec4(a, b);
    }
    """

    FRAG_SHADER = """
    #version 120
    varying vec4 v_color;
    varying vec3 v_index;
    varying vec2 v_position;
    varying vec4 v_ab;
    void main() {
        gl_FragColor = v_color;
        // Discard the fragments between the signals (emulate glMultiDrawArrays).
        if ((fract(v_index.x) > 0.) || (fract(v_index.y) > 0.))
            discard;
        // Clipping test.
        vec2 test = abs((v_position.xy-v_ab.zw)/v_ab.xy);
        if ((test.x > 1) || (test.y > 1))
            discard;
    }
    """


    class Canvas(app.Canvas):
        def __init__(self):
            app.Canvas.__init__(self, title='Use your wheel to zoom!',
                                app='pyqt5', keys='interactive')
            self.program = gloo.Program(VERT_SHADER, FRAG_SHADER)
            self.program['a_position'] = y.reshape(-1, 1)
            self.program['a_color'] = color
            self.program['a_index'] = index
            self.program['u_scale'] = (1., 1.)
            self.program['u_size'] = (nrows, ncols)
            self.program['u_n'] = n

            gloo.set_viewport(0, 0, *self.physical_size)

            self._timer = app.Timer('auto', connect=self.on_timer, start=True)

            gloo.set_state(clear_color='black', blend=True,
                           blend_func=('src_alpha', 'one_minus_src_alpha'))

            self.show()

        def on_resize(self, event):
            gloo.set_viewport(0, 0, *event.physical_size)

        def on_mouse_wheel(self, event):
            dx = np.sign(event.delta[1]) * .05
            scale_x, scale_y = self.program['u_scale']
            scale_x_new, scale_y_new = (scale_x * math.exp(2.5*dx),
                                        scale_y * math.exp(0.0*dx))
            self.program['u_scale'] = (max(1, scale_x_new), max(1, scale_y_new))
            self.update()

        def on_timer(self, event):
            """Add some data at the end of each signal (real-time signals)."""
            k = 10
            y[:, :-k] = y[:, k:]
            y[:, -k:] = amplitudes * np.random.randn(m, k)

            self.program['a_position'].set_data(y.ravel().astype(np.float32))
            self.update()

        def on_draw(self, event):
            gloo.clear()
            self.program.draw('line_strip')

    if __name__ == '__main__':
        c = Canvas()
        app.run()


def test_points_cloud():

    """
    Demonstrating a cloud of points.
    """

    import numpy as np

    from vispy import gloo
    from vispy import app
    from vispy.util.transforms import perspective, translate, rotate

    vert = """
    #version 120
    // Uniforms
    // ------------------------------------
    uniform mat4 u_model;
    uniform mat4 u_view;
    uniform mat4 u_projection;
    uniform float u_linewidth;
    uniform float u_antialias;
    uniform float u_size;
    // Attributes
    // ------------------------------------
    attribute vec3  a_position;
    attribute vec4  a_fg_color;
    attribute vec4  a_bg_color;
    attribute float a_size;
    // Varyings
    // ------------------------------------
    varying vec4 v_fg_color;
    varying vec4 v_bg_color;
    varying float v_size;
    varying float v_linewidth;
    varying float v_antialias;
    void main (void) {
        v_size = a_size * u_size;
        v_linewidth = u_linewidth;
        v_antialias = u_antialias;
        v_fg_color  = a_fg_color;
        v_bg_color  = a_bg_color;
        gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
        gl_PointSize = v_size + 2*(v_linewidth + 1.5*v_antialias);
    }
    """

    frag = """
    #version 120
    // Constants
    // ------------------------------------
    // Varyings
    // ------------------------------------
    varying vec4 v_fg_color;
    varying vec4 v_bg_color;
    varying float v_size;
    varying float v_linewidth;
    varying float v_antialias;
    // Functions
    // ------------------------------------
    // ----------------
    float disc(vec2 P, float size)
    {
        float r = length((P.xy - vec2(0.5,0.5))*size);
        r -= v_size/2;
        return r;
    }
    // ----------------
    float arrow_right(vec2 P, float size)
    {
        float r1 = abs(P.x -.50)*size + abs(P.y -.5)*size - v_size/2;
        float r2 = abs(P.x -.25)*size + abs(P.y -.5)*size - v_size/2;
        float r = max(r1,-r2);
        return r;
    }
    // ----------------
    float ring(vec2 P, float size)
    {
        float r1 = length((gl_PointCoord.xy - vec2(0.5,0.5))*size) - v_size/2;
        float r2 = length((gl_PointCoord.xy - vec2(0.5,0.5))*size) - v_size/4;
        float r = max(r1,-r2);
        return r;
    }
    // ----------------
    float clober(vec2 P, float size)
    {
        const float PI = 3.14159265358979323846264;
        const float t1 = -PI/2;
        const vec2  c1 = 0.2*vec2(cos(t1),sin(t1));
        const float t2 = t1+2*PI/3;
        const vec2  c2 = 0.2*vec2(cos(t2),sin(t2));
        const float t3 = t2+2*PI/3;
        const vec2  c3 = 0.2*vec2(cos(t3),sin(t3));
        float r1 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c1)*size);
        r1 -= v_size/3;
        float r2 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c2)*size);
        r2 -= v_size/3;
        float r3 = length((gl_PointCoord.xy- vec2(0.5,0.5) - c3)*size);
        r3 -= v_size/3;
        float r = min(min(r1,r2),r3);
        return r;
    }
    // ----------------
    float square(vec2 P, float size)
    {
        float r = max(abs(gl_PointCoord.x -.5)*size,
                      abs(gl_PointCoord.y -.5)*size);
        r -= v_size/2;
        return r;
    }
    // ----------------
    float diamond(vec2 P, float size)
    {
        float r = abs(gl_PointCoord.x -.5)*size + abs(gl_PointCoord.y -.5)*size;
        r -= v_size/2;
        return r;
    }
    // ----------------
    float vbar(vec2 P, float size)
    {
        float r1 = max(abs(gl_PointCoord.x -.75)*size,
                       abs(gl_PointCoord.x -.25)*size);
        float r3 = max(abs(gl_PointCoord.x -.5)*size,
                       abs(gl_PointCoord.y -.5)*size);
        float r = max(r1,r3);
        r -= v_size/2;
        return r;
    }
    // ----------------
    float hbar(vec2 P, float size)
    {
        float r2 = max(abs(gl_PointCoord.y -.75)*size,
                       abs(gl_PointCoord.y -.25)*size);
        float r3 = max(abs(gl_PointCoord.x -.5)*size,
                       abs(gl_PointCoord.y -.5)*size);
        float r = max(r2,r3);
        r -= v_size/2;
        return r;
    }
    // ----------------
    float cross(vec2 P, float size)
    {
        float r1 = max(abs(gl_PointCoord.x -.75)*size,
                       abs(gl_PointCoord.x -.25)*size);
        float r2 = max(abs(gl_PointCoord.y -.75)*size,
                       abs(gl_PointCoord.y -.25)*size);
        float r3 = max(abs(gl_PointCoord.x -.5)*size,
                       abs(gl_PointCoord.y -.5)*size);
        float r = max(min(r1,r2),r3);
        r -= v_size/2;
        return r;
    }
    // Main
    // ------------------------------------
    void main()
    {
        float size = v_size +2*(v_linewidth + 1.5*v_antialias);
        float t = v_linewidth/2.0-v_antialias;
        float r = disc(gl_PointCoord, size);
        // float r = square(gl_PointCoord, size);
        // float r = ring(gl_PointCoord, size);
        // float r = arrow_right(gl_PointCoord, size);
        // float r = diamond(gl_PointCoord, size);
        // float r = cross(gl_PointCoord, size);
        // float r = clober(gl_PointCoord, size);
        // float r = hbar(gl_PointCoord, size);
        // float r = vbar(gl_PointCoord, size);
        float d = abs(r) - t;
        if( r > (v_linewidth/2.0+v_antialias))
        {
            discard;
        }
        else if( d < 0.0 )
        {
           gl_FragColor = v_fg_color;
        }
        else
        {
            float alpha = d/v_antialias;
            alpha = exp(-alpha*alpha);
            if (r > 0)
                gl_FragColor = vec4(v_fg_color.rgb, alpha*v_fg_color.a);
            else
                gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
        }
    }
    """


    # ------------------------------------------------------------ Canvas class ---
    class Canvas(app.Canvas):

        def __init__(self):
            app.Canvas.__init__(self, keys='interactive', size=(800, 600))
            ps = self.pixel_scale

            # Create vertices
            n = 1000000
            data = np.zeros(n, [('a_position', np.float32, 3),
                                ('a_bg_color', np.float32, 4),
                                ('a_fg_color', np.float32, 4),
                                ('a_size', np.float32, 1)])
            data['a_position'] = 0.45 * np.random.randn(n, 3)
            data['a_bg_color'] = np.random.uniform(0.85, 1.00, (n, 4))
            data['a_fg_color'] = 0, 0, 0, 1
            data['a_size'] = np.random.uniform(5*ps, 10*ps, n)
            u_linewidth = 1.0
            u_antialias = 1.0

            self.translate = 5
            self.program = gloo.Program(vert, frag)
            self.view = translate((0, 0, -self.translate))
            self.model = np.eye(4, dtype=np.float32)
            self.projection = np.eye(4, dtype=np.float32)

            self.apply_zoom()

            self.program.bind(gloo.VertexBuffer(data))
            self.program['u_linewidth'] = u_linewidth
            self.program['u_antialias'] = u_antialias
            self.program['u_model'] = self.model
            self.program['u_view'] = self.view
            self.program['u_size'] = 5 / self.translate

            self.theta = 0
            self.phi = 0

            gloo.set_state('translucent', clear_color='white')

            self.timer = app.Timer('auto', connect=self.on_timer, start=True)

            self.show()

        def on_key_press(self, event):
            if event.text == ' ':
                if self.timer.running:
                    self.timer.stop()
                else:
                    self.timer.start()

        def on_timer(self, event):
            self.theta += .5
            self.phi += .5
            self.model = np.dot(rotate(self.theta, (0, 0, 1)),
                                rotate(self.phi, (0, 1, 0)))
            self.program['u_model'] = self.model
            self.update()

        def on_resize(self, event):
            self.apply_zoom()

        def on_mouse_wheel(self, event):
            self.translate -= event.delta[1]
            self.translate = max(2, self.translate)
            self.view = translate((0, 0, -self.translate))

            self.program['u_view'] = self.view
            self.program['u_size'] = 5 / self.translate
            self.update()

        def on_draw(self, event):
            gloo.clear()
            self.program.draw('points')

        def apply_zoom(self):
            gloo.set_viewport(0, 0, self.physical_size[0], self.physical_size[1])
            self.projection = perspective(45.0, self.size[0] /
                                          float(self.size[1]), 1.0, 1000.0)
            self.program['u_projection'] = self.projection


    if __name__ == '__main__':
        c = Canvas()
        app.run()


def test_typing():

    def display_string(s: str):
        print(s)
        return

    display_string('hello')
    display_string(3)


# Go!!!
if __name__ == '__main__':
    # test_native()
    # test_signal()
    # test_points_cloud()
    test_typing()
    # test_user()
    # qt_hello_world()
