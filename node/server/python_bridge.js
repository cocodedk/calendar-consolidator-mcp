/**
 * Python worker bridge module.
 * Executes Python scripts and handles IPC communication.
 */

import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DEFAULT_PYTHON = process.platform === 'win32' ? 'python' : 'python3';
const PYTHON_PATH = process.env.PYTHON_PATH || DEFAULT_PYTHON;
const PATH_DELIMITER = path.delimiter;
const PROJECT_ROOT = path.join(__dirname, '../..');

export const PYTHON_COMMAND = PYTHON_PATH;

export function buildPythonEnv() {
  const env = { ...process.env };
  env.PYTHONPATH = env.PYTHONPATH
    ? `${env.PYTHONPATH}${PATH_DELIMITER}${PROJECT_ROOT}`
    : PROJECT_ROOT;
  return env;
}

/**
 * Execute Python script and return JSON result.
 * @param {string} scriptPath - Path to Python script
 * @param {Array} args - Command line arguments
 * @returns {Promise<any>} - Parsed JSON result
 */
export async function executePython(scriptPath, args = []) {
  return new Promise((resolve, reject) => {
    // Set PYTHONPATH to include project root
    const env = buildPythonEnv();
    const python = spawn(PYTHON_PATH, [scriptPath, ...args], { env });

    let stdout = '';
    let stderr = '';

    python.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    python.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    python.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}: ${stderr}`));
        return;
      }

      try {
        const result = JSON.parse(stdout);
        resolve(result);
      } catch (e) {
        reject(new Error(`Failed to parse Python output: ${e.message}\nOutput: ${stdout}`));
      }
    });

    python.on('error', (err) => {
      reject(new Error(`Failed to start Python process: ${err.message}`));
    });
  });
}

/**
 * Execute Python module function.
 * @param {string} module - Python module path (e.g., 'python.sync.syncer')
 * @param {string} func - Function name
 * @param {object} params - Parameters as JSON
 * @param {string} className - Optional class name (if calling class method)
 * @returns {Promise<any>} - Result from Python function
 */
export async function callPythonFunction(module, func, params = {}, className = null) {
  const scriptPath = path.join(__dirname, '../../python/cli_wrapper.py');
  const args = [
    '--module', module,
    '--function', func,
    '--params', JSON.stringify(params)
  ];

  if (className) {
    args.push('--class', className);
  }

  return executePython(scriptPath, args);
}

export default {
  executePython,
  callPythonFunction
};
